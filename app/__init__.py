from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, clients, oidc
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="EGAuth - OpenID Connect Provider", version="1.0.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
CORSMiddleware,
allow_origins=['*'], # Jamais '*' en production
allow_methods=['GET', 'POST'],
allow_headers=['Authorization', 'Content-Type'],
)

# Enregistrer tous les routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(users.router)
app.include_router(oidc.router)  # Routes OpenID Connect Discovery
