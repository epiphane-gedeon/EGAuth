from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.client_service import get_client_by_id
from app.services.user_service import authenticate_user
from app.services.token_service import create_authorization_code
import urllib.parse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/template")
 
router = APIRouter(tags=['OAuth2'])
 
@router.get('/authorize')
async def authorize(
    response_type: str = Query(...), client_id: str = Query(...),
    redirect_uri: str  = Query(...), scope: str = Query('openid'),
    state: str = Query(None), nonce: str = Query(None),
    code_challenge: str = Query(None), code_challenge_method: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    client = await get_client_by_id(client_id, db)
    if not client or not client.is_active:
        raise HTTPException(400, 'client_id invalide')
 
    if redirect_uri not in client.redirect_uris:
        raise HTTPException(400, 'redirect_uri non autorisée')
 
    if response_type != 'code':
        raise HTTPException(400, 'response_type doit être code')
 
    html = f'''
    <form method='POST' action='/authorize'>
      <input type='hidden' name='client_id' value='{client_id}'>
      <input type='hidden' name='redirect_uri' value='{redirect_uri}'>
      <input type='hidden' name='scope' value='{scope}'>
      <input type='hidden' name='state' value='{state or ""}'>
      <input type='hidden' name='nonce' value='{nonce or ""}'>
      <input type='hidden' name='code_challenge' value='{code_challenge or ""}'>
      <input type='hidden' name='code_challenge_method' value='{code_challenge_method or ""}'>
      <input type='email' name='email' placeholder='Email' required>
      <input type='password' name='password' placeholder='Mot de passe' required>
      <button type='submit'>Se connecter avec EGAuth</button>
    </form>'''
    # return HTMLResponse(html)
    
    return templates.TemplateResponse({
        # "request": request,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state or "",
        "nonce": nonce or "",
        "code_challenge": code_challenge or "",
        "code_challenge_method": code_challenge_method or ""
    }, "auth.html",{
        # "request": request,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state or "",
        "nonce": nonce or "",
        "code_challenge": code_challenge or "",
        "code_challenge_method": code_challenge_method or ""
    },)
    

# @router.get('/authorize')
# async def authorize(request: Request, client_id: str, redirect_uri: str, scope: str, state: str = "", nonce: str = "", code_challenge: str = "", code_challenge_method: str = ""):
#     return templates.TemplateResponse("auth.html", {
#         "request": request,
#         "client_id": client_id,
#         "redirect_uri": redirect_uri,
#         "scope": scope,
#         "state": state or "",
#         "nonce": nonce or "",
#         "code_challenge": code_challenge or "",
#         "code_challenge_method": code_challenge_method or ""
#     })
 
 
@router.post('/authorize')
async def authorize_submit(
    client_id: str=Form(...), redirect_uri: str=Form(...), scope: str=Form(...),
    state: str=Form(''), nonce: str=Form(''),
    code_challenge: str=Form(''), code_challenge_method: str=Form(''),
    email: str=Form(...), password: str=Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(email, password, db)
    if not user:
        params = urllib.parse.urlencode({'error': 'access_denied', 'state': state})
        return RedirectResponse(f'{redirect_uri}?{params}', status_code=302)
 
    code = await create_authorization_code(
        user_id=str(user.id), client_id=client_id, redirect_uri=redirect_uri,
        scopes=scope.split(),
        code_challenge=code_challenge or None,
        code_challenge_method=code_challenge_method or None, db=db
    )
    params = urllib.parse.urlencode({'code': code, 'state': state})
    return RedirectResponse(f'{redirect_uri}?{params}', status_code=302)

@router.post('/token')
async def token_endpoint(
    request: Request,
    grant_type: str = Form(...), code: str = Form(None),
    redirect_uri: str = Form(None), client_id: str = Form(...),
    client_secret: str = Form(None), code_verifier: str = Form(None),
    refresh_token_val: str = Form(None, alias='refresh_token'),
    db: AsyncSession = Depends(get_db),
):
    from app.security.password import verify_secret
    from app.services.token_service import exchange_code_for_tokens, refresh_access_token
 
    client = await get_client_by_id(client_id, db)
    if not client or not verify_secret(client_secret, client.client_secret_hash):
        raise HTTPException(401, 'Credentials client invalides')
 
    if grant_type == 'authorization_code':
        return await exchange_code_for_tokens(
            code=code, redirect_uri=redirect_uri, client_id=client_id,
            code_verifier=code_verifier, db=db
        )
    elif grant_type == 'refresh_token':
        return await refresh_access_token(
            refresh_token=refresh_token_val, client_id=client_id, db=db
        )
 
    raise HTTPException(400, f'grant_type non supporté: {grant_type}')
