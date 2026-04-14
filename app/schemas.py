from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ClientRegisterRequest(BaseModel):
    name: str
    redirect_uris: List[str]
    allowed_scopes: List[str] = ['openid', 'profile', 'email']

class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
