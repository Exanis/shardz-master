from httpx import AsyncClient, Request, Response
from pytest_httpx import HTTPXMock


async def test_servers_list_not_connected(app):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.get("/servers/")
    assert response.status_code == 401


async def test_servers_list_with_invalid_key(app):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.get(
            "/servers/", headers={"Authorization": "Bearer invalid_token"}
        )
    assert response.status_code == 401


async def test_servers_list_with_invalid_auth_method(app, token):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.get(
            "/servers/", headers={"Authorization": f"Basic {token}"}
        )
    assert response.status_code == 401


async def test_servers_list(app_with_servers, token):
    async with AsyncClient(app=app_with_servers, base_url="http://test/") as ac:
        response = await ac.get(
            "/servers/", headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "World 1",
            "url": "http://world1.test/",
            "status": "online",
            "population": "low",
        },
        {
            "name": "World 2",
            "url": "http://world2.test/",
            "status": "online",
            "population": "medium",
        },
        {
            "name": "World 3",
            "url": "http://world3.test/",
            "status": "offline",
            "population": "high",
        },
        {
            "name": "World 4",
            "url": "http://world4.test/",
            "status": "online",
            "population": "full",
        },
    ]


async def test_servers_list_empty(app, token):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.get(
            "/servers/", headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json() == []


async def test_register_server(app, httpx: HTTPXMock):
    has_been_called = False

    def callback(request: Request):
        nonlocal has_been_called
        has_been_called = True
        assert request.headers["Authorization"] == "Bearer invalid_key"
        assert request.content == b'{"url": "http://world1.test/"}'
        return Response(200, json={"details": "World registered"})

    httpx.add_callback(url="http://servers/register/", callback=callback)

    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post(
            "/servers/",
            json={
                "url": "http://world1.test/",
            },
            headers={"Authorization": "Bearer invalid_key"},
        )
    assert response.status_code == 200
    assert has_been_called
