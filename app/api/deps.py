from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.core.tokens import verify_token
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        token_version = payload.get("ver")
        print("[Get Current User] Token version from payload:", token_version)
        
        if user_id is None:
            raise Exception()
        
        user = db.query(User).filter(User.id == user_id).first()
        print("[Get Current User] Token version from db:", user.token_version)
        if token_version != user.token_version:
            raise HTTPException(status_code=401, detail="Token expired due to password change")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
