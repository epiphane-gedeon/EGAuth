from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.auth_service import register_user, login_user, list_all_users , modify_user
from app.schemas.user import UserCreate, UserUpdate
from app.api.deps import get_current_user

router = APIRouter()
        
@router.get("/")
def read_root():
    return {"message": "Welcome to the Auth API"}

@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user_id": str(current_user.id),
        "email": current_user.email
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    token = register_user(db, user.email, user.password)
    return {"access_token": token}

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = login_user(db, user.email, user.password)
    return {"access_token": token}

@router.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = list_all_users(db)
    
    print(users[1].token_version)
    return users

@router.put("/users/me")
def update_user_me(user_update: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Implement the logic to update the current user's information
    token= modify_user(db, current_user, user_update.email, user_update.password)
    if not token:
        return {
        "message": "User updated successfully"
    }
    return {
        "message": "User updated successfully",
        "access_token": token
    }