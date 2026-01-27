from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

# ALGORITHM = "RS256"

with open("private.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("public.pem", "r") as f:
    PUBLIC_KEY = f.read()

def create_access_token(user_id: str, token_version: int = 0):
    payload = {
        "sub": str(user_id),
        "ver" : token_version,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str):
    return jwt.decode(token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])