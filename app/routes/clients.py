from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.services.client_service import register_client
from app.schemas import ClientRegisterRequest

router = APIRouter(prefix="/clients", tags=["Clients OAuth"])


@router.get("/register-form", response_class=HTMLResponse)
async def register_client_form():
    """Affiche le formulaire d'enregistrement client OAuth"""
    with open("app/template/register_client.html", "r") as f:
        return f.read()


@router.post("/register")
async def register_oauth_client(data: ClientRegisterRequest, db=Depends(get_db)):
    client, secret = await register_client(data, db)
    return {
        "client_id": client.client_id,
        "client_secret": secret,  # Sauvegardez-le maintenant !
        "name": client.name,
        "redirect_uris": client.redirect_uris,
        "allowed_scopes": client.allowed_scopes,
    }
