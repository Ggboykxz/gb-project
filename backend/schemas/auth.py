"""Pydantic schemas for authentication module"""
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
    role: UserRole = UserRole.ETUDIANT


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TOTPSetupResponse(BaseModel):
    totp_uri: str
    qr_code_base64: str
    secret: str


class VerifyTOTPRequest(BaseModel):
    totp_code: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
