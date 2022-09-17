"""
Authentication-related routes. They will manage the login / logout of users
but not administration (nor users creation).
"""
from pydantic import BaseModel
from httpx import AsyncClient
from fastapi import Request, HTTPException, Depends
from fastapi_utils.inferring_router import InferringRouter
from server.settings import settings
from server.tools import try_login_player, disconnect_player, require_api


router = InferringRouter(
    prefix="/login",
    tags=["Authentication"],
)


class TokenResponse(BaseModel):
    """
    A token response is a simple string containing the token.
    """

    token: str


@router.post("/")
async def login(request: Request) -> TokenResponse:
    """
    Returns a token to be used for authentication

    :param request: FastAPI's request object (automatically injected)
    :return: A token to be used for authentication.
    :raises HTTPException: 400 player alread logged, 401 invalid credentials
    """
    params = await request.json()
    async with AsyncClient(base_url=settings.identification_url) as client:
        response = await client.post("/login/", json=params)
    if response.status_code == 200:
        player_identifier = response.json()["identifier"]
        token = try_login_player(player_identifier)
        if token:
            return TokenResponse(token=token)
        raise HTTPException(status_code=400, detail="Already connected")
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout/")
async def logout(data: TokenResponse, _: str = Depends(require_api)):
    """
    Logs out a user

    :param data: The token of the user to log out.
    :param _: The API key (automatically injected).
    :return: A message confirming the logout.
    :raises HTTPException: 404 If the token is invalid.
    """
    if disconnect_player(data.token):
        return {"detail": "Player disconnected"}
    raise HTTPException(status_code=404, detail="Player not found")
