"""
Generic tools to deal with authorization.
"""
from fastapi import Header, HTTPException, Depends
from server.settings import settings


def authorization_key(authorization: str = Header(default=None)) -> str:
    """
    Return the authorization key

    :param authorization: The authorization header (automatically injected)
    :return: The authorization key
    :raises HTTPException: 401 If the authorization header is missing or invalid.
    """
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    params = authorization.split(" ")
    auth_type = params[0]
    token = params[1]
    if auth_type != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return token


def require_api(token: str = Depends(authorization_key)) -> None:
    """
    Require a valid API key

    :param token: The authorization key (automatically injected)
    :raises HTTPException: 401 If the API key is invalid.
    """
    if token != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid token")
