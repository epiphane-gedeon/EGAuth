from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.services.user_service import create_user
from app.schemas import UserRegisterRequest, UserResponse

templates = Jinja2Templates(directory="app/template")

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/register-form", response_class=HTMLResponse)
async def register_form():
    """Affiche le formulaire d'enregistrement utilisateur"""
    with open("app/template/register_user.html", "r") as f:
        return f.read()


@router.post("/register", response_model=UserResponse)
async def register_user_endpoint(data: UserRegisterRequest, db=Depends(get_db)):
    user = await create_user(data, db)
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
