import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import OAuthClient
from app.security.password import hash_secret

async def register_client(data, db: AsyncSession) -> tuple[OAuthClient, str]:
    client_id     = f'egauth_{secrets.token_urlsafe(16)}'
    client_secret = secrets.token_urlsafe(48)   # Retourné une seule fois
 
    client = OAuthClient(
        client_id=client_id,
        client_secret_hash=hash_secret(client_secret),  # Jamais en clair !
        name=data.name,
        redirect_uris=data.redirect_uris,
        allowed_scopes=data.allowed_scopes,
    )
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client, client_secret

async def get_client_by_id(client_id: str, db: AsyncSession) -> OAuthClient | None:
    result = await db.execute(select(OAuthClient).where(OAuthClient.client_id == client_id))
    return result.scalar_one_or_none()
