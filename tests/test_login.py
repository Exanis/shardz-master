from httpx import AsyncClient


async def test_connect(app):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post("/login/", json={"credentials": "valid"})
    assert response.status_code == 200
    result = response.json()
    assert result.get("token", None) != None


async def test_connect_invalid_credentials(app):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post("/login/", json={"credentials": "invalid"})
    assert response.status_code == 401


async def test_connect_when_already_connected(app):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post("/login/", json={"credentials": "valid"})
        response = await ac.post("/login/", json={"credentials": "valid"})
    assert response.status_code == 400
