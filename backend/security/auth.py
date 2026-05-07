"""Security utilities for GabonEdu Campus - Authentification JWT, 2FA TOTP, RBAC"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import pyotp
import qrcode
import base64
from io import BytesIO
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User, Role
from models.securite import SessionUtilisateur, TentativeConnexion

# Configuration
SECRET_KEY = "gabonedu-secret-key-change-in-production-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password with Argon2"""
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength according to GabonEdu policy:
    - Min 8 characters
    - At least 1 uppercase
    - At least 1 digit
    - At least 1 special character
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, "Mot de passe valide"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify a token and check its type"""
    payload = decode_token(token)
    if payload is None:
        return None
    
    if payload.get("type") != token_type:
        return None
    
    return payload


def create_totp_secret() -> str:
    """Generate a new TOTP secret"""
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str, issuer: str = "GabonEdu Campus") -> str:
    """Generate TOTP URI for QR code"""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=issuer)


def generate_totp_qr_code(totp_uri: str) -> str:
    """Generate QR code for TOTP setup as base64 string"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


def verify_totp(secret: str, code: str) -> bool:
    """Verify a TOTP code"""
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)  # 1 window tolerance


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current authenticated user from JWT token"""
    token_data = decode_token(token)
    if token_data is None or token_data.get("type") != "access":
        return None
    
    user_id = token_data.get("sub")
    if user_id is None:
        return None
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None or not user.is_active:
        return None
    
    return user


async def check_account_lockout(email: str, db: AsyncSession) -> bool:
    """Check if account is locked due to too many failed attempts"""
    thirty_min_ago = datetime.utcnow() - timedelta(minutes=30)
    result = await db.execute(
        select(TentativeConnexion).where(
            TentativeConnexion.email == email,
            TentativeConnexion.succes == False,
            TentativeConnexion.date_essai >= thirty_min_ago
        )
    )
    failed_attempts = result.scalars().all()
    return len(failed_attempts) >= 5


async def record_login_attempt(email: str, success: bool, db: AsyncSession, ip_address: str = "127.0.0.1"):
    """Record login attempt"""
    attempt = TentativeConnexion(
        email=email,
        succes=success,
        adresse_ip=ip_address
    )
    db.add(attempt)
    await db.commit()


async def invalidate_user_sessions(user_id: int, db: AsyncSession, current_session_id: Optional[int] = None):
    """Invalidate all user sessions except optionally one"""
    query = SessionUtilisateur.__table__.update().where(
        SessionUtilisateur.utilisateur_id == user_id
    )
    
    if current_session_id:
        query = query.where(SessionUtilisateur.id != current_session_id)
    
    query = query.values(statut="invalide", date_expiration=datetime.utcnow())
    await db.execute(query)
    await db.commit()


def require_permission(permission: str):
    """
    Dependency factory to check if user has required permission.
    Usage: @require_permission("notes:validate")
    """
    async def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non authentifié"
            )
        
        # SUPER_ADMIN and ADMIN_SCOL have all permissions
        if current_user.role in [Role.SUPER_ADMIN, Role.ADMIN_SCOL]:
            return current_user
        
        # Simple permission check based on role
        role_permissions = {
            Role.ENSEIGNANT: ["notes:create", "notes:update", "cours:read", "presence:create"],
            Role.ETUDIANT: ["portfolio:read", "portfolio:update", "candidatures:create"],
            Role.FINANCIER: ["finances:read", "finances:create", "paiements:validate"],
            Role.BIBLIOTHECAIRE: ["bibliotheque:read", "bibliotheque:update"],
            Role.CHERCHEUR: ["recherche:read", "recherche:create"],
        }
        
        user_permissions = role_permissions.get(current_user.role, [])
        
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission insuffisante: {permission} requise"
            )
        
        return current_user
    
    return permission_checker
