from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import get_settings
from app.security.rsa_keys import load_or_create_keys
import uuid
 
settings = get_settings()
PRIVATE_KEY, PUBLIC_KEY = load_or_create_keys(
    settings.PRIVATE_KEY_PATH, settings.PUBLIC_KEY_PATH
)
ISSUER = 'http://localhost:8000'
 
def create_access_token(user_id: str, scopes: list[str], client_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'iss': ISSUER,
        'sub': user_id,
        'aud': client_id,
        'iat': now,
        'exp': now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        'jti': str(uuid.uuid4()),
        'scope': ' '.join(scopes),
        'token_type': 'access',
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
 
def create_id_token(user, scopes: list[str], client_id: str, nonce: str = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'iss': ISSUER, 'sub': str(user.id), 'aud': client_id,
        'iat': now, 'exp': now + timedelta(hours=1), 'nonce': nonce,
    }
    if 'profile' in scopes:
        payload['preferred_username'] = user.username
        payload['name'] = f'{user.first_name or ""} {user.last_name or ""}'.strip()
    if 'email' in scopes:
        payload['email'] = user.email
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
 
def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'],
                          options={'verify_aud': False})
    except JWTError as e:
        raise ValueError(f'Token invalide: {e}')
