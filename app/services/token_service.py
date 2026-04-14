import secrets, hashlib, base64
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.models import AuthorizationCode, RefreshToken, User
from app.security.jwt_handler import create_access_token, create_id_token
from fastapi import HTTPException
 
async def create_authorization_code(
    user_id, client_id, redirect_uri, scopes,
    code_challenge, code_challenge_method, db
) -> str:
    code_value = secrets.token_urlsafe(48)
    db.add(AuthorizationCode(
        code=code_value, user_id=user_id, client_id=client_id,
        redirect_uri=redirect_uri, scopes=scopes,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    ))
    await db.commit()
    return code_value
 
 
async def exchange_code_for_tokens(
    code, redirect_uri, client_id, code_verifier, db
) -> dict:
    result = await db.execute(select(AuthorizationCode).where(
        AuthorizationCode.code == code))
    auth_code = result.scalar_one_or_none()
 
    if not auth_code: 
        raise HTTPException(400, 'Code invalide')
    if auth_code.used: 
        raise HTTPException(400, 'Code déjà utilisé')
    if auth_code.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, 'Code expiré')
    if auth_code.client_id != client_id:
        raise HTTPException(400, 'client_id incorrect')
    if auth_code.redirect_uri != redirect_uri:
        raise HTTPException(400, 'redirect_uri incorrect')
 
    if auth_code.code_challenge:
        if not code_verifier: 
            raise HTTPException(400, 'code_verifier requis')
        digest    = hashlib.sha256(code_verifier.encode()).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
        if challenge != auth_code.code_challenge:
            raise HTTPException(400, 'PKCE invalide')
 
    auth_code.used = True
    await db.commit()
 
    user = await db.get(User, auth_code.user_id)
    access_token = create_access_token(str(user.id), auth_code.scopes, client_id)
 
    rt_value = secrets.token_urlsafe(64)
    db.add(RefreshToken(
        token=rt_value, user_id=user.id, client_id=client_id,
        scopes=auth_code.scopes,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    ))
    await db.commit()
 
    response = {
        'access_token': access_token, 'token_type': 'Bearer',
        'expires_in': 1800, 'refresh_token': rt_value,
    }
    if 'openid' in auth_code.scopes:
        response['id_token'] = create_id_token(user, auth_code.scopes, client_id)
    return response

async def refresh_access_token(refresh_token: str, client_id: str, db) -> dict:
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == refresh_token))
    rt = result.scalar_one_or_none()
 
    if not rt: 
        raise HTTPException(400, 'Refresh token invalide')
    if rt.is_revoked:
        await revoke_all_user_tokens(rt.user_id, rt.client_id, db)
        raise HTTPException(400, 'Token compromis — réauthentification requise')
    if rt.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, 'Refresh token expiré')
 
    rt.is_revoked = True
    user = await db.get(User, rt.user_id)
 
    new_access = create_access_token(str(user.id), rt.scopes, client_id)
    new_rt_val = secrets.token_urlsafe(64)
    db.add(RefreshToken(
        token=new_rt_val, user_id=user.id, client_id=client_id,
        scopes=rt.scopes,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    ))
    await db.commit()
 
    return {
        'access_token': new_access, 'token_type': 'Bearer',
        'expires_in': 1800, 'refresh_token': new_rt_val,
    }
 
async def revoke_all_user_tokens(user_id, client_id, db):
    from sqlalchemy import update
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .where(RefreshToken.client_id == client_id)
        .values(is_revoked=True)
    )
    await db.commit()
