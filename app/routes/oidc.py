from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db
from app.security.jwt_handler import verify_access_token
from app.models import User
import uuid
 
router = APIRouter(tags=['OpenID Connect'])
bearer = HTTPBearer()
 
@router.get('/userinfo')
async def userinfo(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db = Depends(get_db),
):
    try:
        payload = verify_access_token(creds.credentials)
    except ValueError:
        raise HTTPException(401, 'Token invalide')
 
    user = await db.get(User, uuid.UUID(payload['sub']))
    if not user: 
        raise HTTPException(404, 'Utilisateur introuvable')
 
    scopes   = payload.get('scope', '').split()
    response = {'sub': str(user.id)}
    if 'profile' in scopes:
        response['preferred_username'] = user.username
        response['name'] = f'{user.first_name or ""} {user.last_name or ""}'.strip()
    if 'email' in scopes:
        response['email']          = user.email
        response['email_verified'] = user.is_verified
    return response

@router.get('/.well-known/jwks.json')
async def jwks():
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from app.security.rsa_keys import load_or_create_keys
    from app.config import get_settings
    import base64
 
    settings = get_settings()
    _, pub_pem = load_or_create_keys(settings.PRIVATE_KEY_PATH, settings.PUBLIC_KEY_PATH)
    pub_key = load_pem_public_key(pub_pem)
    numbers = pub_key.public_numbers()
 
    def b64url(n: int) -> str:
        length = (n.bit_length() + 7) // 8
        return base64.urlsafe_b64encode(n.to_bytes(length, 'big')).rstrip(b'=').decode()
 
    return {'keys': [{'kty': 'RSA', 'use': 'sig', 'alg': 'RS256',
                       'kid': 'egauth-key-1',
                       'n': b64url(numbers.n), 'e': b64url(numbers.e)}]}
 
 
@router.get('/.well-known/openid-configuration')
async def oidc_discovery():
    base = 'http://localhost:8000'
    return {
        'issuer':                 base,
        'authorization_endpoint': f'{base}/authorize',
        'token_endpoint':         f'{base}/token',
        'userinfo_endpoint':      f'{base}/userinfo',
        'jwks_uri':               f'{base}/.well-known/jwks.json',
        'response_types_supported':               ['code'],
        'id_token_signing_alg_values_supported':  ['RS256'],
        'scopes_supported': ['openid','profile','email','offline_access'],
        'code_challenge_methods_supported':       ['S256'],
    }
