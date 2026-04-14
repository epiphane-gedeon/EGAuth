from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, users, clients, oidc

app = FastAPI(title="EGAuth - OpenID Connect Provider", version="1.0.0")

app.add_middleware(
CORSMiddleware,
allow_origins=['https://votreapp.com'], # Jamais '*' en production
allow_methods=['GET', 'POST'],
allow_headers=['Authorization', 'Content-Type'],
)

# Enregistrer tous les routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(users.router)
app.include_router(oidc.router)  # Routes OpenID Connect Discovery

@app.on_event('startup')
async def startup():
    from app.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)