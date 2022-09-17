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
    """Returns a token to be used for authentication"""
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
    """Logs out a user"""
    if disconnect_player(data.token):
        return {"detail": "Player disconnected"}
    raise HTTPException(status_code=404, detail="Player not found")
