from sqlalchemy import select
from app.models import User
from app.security.password import hash_password, verify_password
from fastapi import HTTPException, status
 
async def create_user(data, db) -> User:
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(409, 'Email déjà utilisé')
 
    user = User(
        email=data.email, username=data.username,
        hashed_password=hash_password(data.password),
        first_name=data.first_name, last_name=data.last_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
 
 
async def authenticate_user(email: str, password: str, db) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user   = result.scalar_one_or_none()
 
    if not user or not verify_password(password, user.hashed_password):
        return None   # Ne pas indiquer lequel est faux (timing attack)
 
    if not user.is_active:
        raise HTTPException(403, 'Compte désactivé')
 
    return user
