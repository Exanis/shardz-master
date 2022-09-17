"""
Servers management module.
"""
from typing import List
from pydantic import BaseModel
from httpx import AsyncClient
from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from server.settings import settings
from server.tools import require_user, require_api


router = InferringRouter(prefix="/servers", tags=["Servers"])


class Server(BaseModel):
    """
    A server is a game server.
    """

    name: str
    url: str
    status: str
    population: str


@router.get("/")
async def list_servers(_: str = Depends(require_user)) -> List[Server]:
    """
    Returns the list of servers.

    :param _: The user name (automatically injected).
    :return: The list of servers.
    """
    async with AsyncClient(base_url=settings.servers_url) as client:
        response = await client.get("/list/")
    return [Server(**server) for server in response.json()]


class ServerRegisterData(BaseModel):
    """
    Data to register a new server.
    """

    url: str


@router.post("/")
async def register_server(data: ServerRegisterData, _: str = Depends(require_api)):
    """
    Registers a new server.

    :param data: The url of the server to register
    :param _: The API key (automatically injected).
    :return: A message confirming the registration.
    """
    async with AsyncClient(base_url=settings.servers_url) as client:
        await client.post(
            "/register/",
            json=data.dict(),
            headers={"Authorization": f"Bearer {settings.api_key}"},
        )
    return {"detail": "World registered"}
