from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password
from app.core.tokens import create_access_token
from app.crud.user import get_user_by_email, create_user, get_all_users, update_user
from app.models.user import User

def register_user(db, email: str, password: str):
    if get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = create_user(db, email, hash_password(password))
    
    return create_access_token(user.id, user.token_version)

def login_user(db, email, password):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return create_access_token(user.id, user.token_version)


def modify_user(db, user: User, email=None, password=None):

    if email:
        if get_user_by_email(db, email) and email != user.email:
            raise HTTPException(status_code=409, detail="Email already used")
        user.email = email

    if password:
        user.password_hash = hash_password(password)
        user.token_version += 1  # Invalidate existing tokens
        update_user(db, user)
        return create_access_token(user.id, user.token_version)
    
    update_user(db, user)
    # return user

def list_all_users(db):
    return get_all_users(db)
