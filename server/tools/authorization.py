"""
Generic tools to deal with authorization.
"""
from fastapi import Header, HTTPException, Depends
from server.settings import settings


def authorization_key(authorization: str = Header(default=None)) -> str:
    """Return the authorization key"""
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    params = authorization.split(" ")
    auth_type = params[0]
    token = params[1]
    if auth_type != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return token


def require_api(token: str = Depends(authorization_key)) -> None:
    """Require a valid API key"""
    if token != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid token")
