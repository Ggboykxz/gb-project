"""Pydantic schemas for authentication module - GabonEdu Campus"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN_SCOL = "ADMIN_SCOL"
    ENSEIGNANT = "ENSEIGNANT"
    ETUDIANT = "ETUDIANT"
    FINANCIER = "FINANCIER"
    BIBLIOTHECAIRE = "BIBLIOTHECAIRE"
    CHERCHEUR = "CHERCHEUR"


class UserBase(BaseModel):
    email: EmailStr
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    role: Optional[UserRole] = UserRole.ETUDIANT


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserProfile(BaseModel):
    id: str
    email: str
    nom: str
    prenom: str
    role: UserRole
    is_active: bool
    is_verified: Optional[bool] = False
    has_totp: Optional[bool] = False
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes


class TOTPSetupResponse(BaseModel):
    secret: str
    uri: str
    qr_code: str
    message: str


class TOTPVerifyRequest(BaseModel):
    secret: Optional[str] = None
    code: str


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
