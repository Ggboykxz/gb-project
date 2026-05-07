"""
Router d'authentification pour GabonEdu Campus.
Gère login, logout, refresh token, 2FA TOTP, gestion de session.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User, Role
from models.securite import SessionUtilisateur
from schemas.auth import (
    UserCreate, UserLogin, TokenResponse, UserProfile, 
    TOTPSetupResponse, TOTPVerifyRequest, PasswordChangeRequest
)
from security.auth import (
    verify_password, get_password_hash, validate_password_strength,
    create_access_token, create_refresh_token, decode_token,
    create_totp_secret, get_totp_uri, generate_totp_qr_code, verify_totp,
    get_current_user, check_account_lockout, record_login_attempt,
    invalidate_user_sessions
)

router = APIRouter(tags=["Authentification"])


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Enregistrer un nouvel utilisateur.
    Validation du mot de passe + création avec rôle par défaut.
    """
    # Vérifier si l'email existe déjà
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )
    
    # Valider la force du mot de passe
    is_valid, error_msg = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Créer l'utilisateur
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        nom=user_data.nom,
        prenom=user_data.prenom,
        role=user_data.role or Role.ETUDIANT,
        is_active=True,
        is_verified=False
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return UserProfile(
        id=new_user.id,
        email=new_user.email,
        nom=new_user.nom,
        prenom=new_user.prenom,
        role=new_user.role,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    """
    Authentification utilisateur.
    Retourne access_token + refresh_token.
    Supporte le 2FA TOTP si activé.
    """
    email = form_data.username
    password = form_data.password
    
    # Vérifier si le compte est verrouillé
    is_locked = await check_account_lockout(email, db)
    if is_locked:
        await record_login_attempt(email, False, db, request.client.host if request else "127.0.0.1")
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Compte temporairement verrouillé. Réessayez dans 30 minutes."
        )
    
    # Récupérer l'utilisateur
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        await record_login_attempt(email, False, db, request.client.host if request else "127.0.0.1")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        await record_login_attempt(email, False, db, request.client.host if request else "127.0.0.1")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    # Vérifier si 2FA est activé
    if user.totp_secret:
        # Le code TOTP doit être fourni dans le champ 'totp_code' du form
        totp_code = form_data.extra.get("totp_code", None) if hasattr(form_data, 'extra') else None
        if not totp_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code 2FA requis. Veuillez fournir le code TOTP."
            )
        
        if not verify_totp(user.totp_secret, totp_code):
            await record_login_attempt(email, False, db, request.client.host if request else "127.0.0.1")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Code 2FA invalide"
            )
    
    # Succès - enregistrer la tentative
    await record_login_attempt(email, True, db, request.client.host if request else "127.0.0.1")
    
    # Invalider les autres sessions (session unique par poste)
    await invalidate_user_sessions(user.id, db)
    
    # Créer une nouvelle session
    session = SessionUtilisateur(
        utilisateur_id=user.id,
        jeton_refresh=create_refresh_token({"sub": str(user.id)}),
        date_connexion=datetime.utcnow(),
        adresse_ip=request.client.host if request else "127.0.0.1",
        statut="active"
    )
    db.add(session)
    await db.commit()
    
    # Mettre à jour last_login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Générer les tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=900  # 15 minutes
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Rafraîchir un token d'accès expiré.
    """
    payload = decode_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré"
        )
    
    user_id = int(payload.get("sub"))
    
    # Vérifier que la session existe et est active
    result = await db.execute(
        select(SessionUtilisateur).where(
            SessionUtilisateur.utilisateur_id == user_id,
            SessionUtilisateur.jeton_refresh == refresh_token,
            SessionUtilisateur.statut == "active"
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session invalide"
        )
    
    # Vérifier que l'utilisateur existe toujours et est actif
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inexistant ou désactivé"
        )
    
    # Générer un nouveau token d'accès
    new_access_token = create_access_token(data={"sub": str(user_id)})
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=900
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Déconnexion utilisateur - invalide la session courante.
    """
    # Invalider toutes les sessions de cet utilisateur
    await invalidate_user_sessions(current_user.id, db)
    
    return {"message": "Déconnexion réussie"}


@router.get("/me", response_model=UserProfile)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Récupérer le profil de l'utilisateur connecté.
    """
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        nom=current_user.nom,
        prenom=current_user.prenom,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        has_totp=bool(current_user.totp_secret),
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.post("/totp/setup", response_model=TOTPSetupResponse)
async def setup_totp(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Configurer l'authentification 2FA TOTP.
    Génère un secret et un QR Code pour l'enrôlement.
    """
    if current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA déjà configuré pour cet utilisateur"
        )
    
    # Générer un nouveau secret TOTP
    secret = create_totp_secret()
    uri = get_totp_uri(secret, current_user.email)
    qr_code = generate_totp_qr_code(uri)
    
    # Stocker temporairement le secret dans la session (à implémenter)
    # Pour l'instant, on le retourne au client qui devra le renvoyer pour vérification
    
    return TOTPSetupResponse(
        secret=secret,
        uri=uri,
        qr_code=qr_code,
        message="Scannez ce QR code avec votre application d'authentification (Google Authenticator, Authy, etc.)"
    )


@router.post("/totp/verify")
async def verify_totp_setup(
    data: TOTPVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Vérifier et activer le 2FA TOTP après configuration.
    """
    if not current_user.totp_secret:
        # Premier enrôlement - le secret est fourni dans la requête
        if not verify_totp(data.secret, data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code TOTP invalide"
            )
        
        # Activer le 2FA
        current_user.totp_secret = data.secret
        current_user.is_verified = True
        await db.commit()
        
        return {"message": "2FA activé avec succès"}
    else:
        # Vérification normale avec secret existant
        if not verify_totp(current_user.totp_secret, data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code TOTP invalide"
            )
        
        return {"message": "Code 2FA vérifié avec succès"}


@router.post("/totp/disable")
async def disable_totp(
    data: TOTPVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Désactiver le 2FA TOTP (nécessite un code valide).
    """
    if not current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA n'est pas activé"
        )
    
    if not verify_totp(current_user.totp_secret, data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code TOTP invalide"
        )
    
    current_user.totp_secret = None
    await db.commit()
    
    return {"message": "2FA désactivé avec succès"}


@router.post("/password/change")
async def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Changer son mot de passe.
    """
    # Vérifier l'ancien mot de passe
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ancien mot de passe incorrect"
        )
    
    # Valider le nouveau mot de passe
    is_valid, error_msg = validate_password_strength(data.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Vérifier que l'ancien et le nouveau sont différents
    if data.old_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nouveau mot de passe doit être différent de l'ancien"
        )
    
    # Mettre à jour le mot de passe
    current_user.hashed_password = get_password_hash(data.new_password)
    await db.commit()
    
    return {"message": "Mot de passe changé avec succès"}
