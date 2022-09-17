from httpx import AsyncClient


async def test_disconnect_user_without_key(app, token):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post("/login/logout/", json={"token": token})
    assert response.status_code == 401


async def test_disconnect_user_with_invalid_key(app, token):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post(
            "/login/logout/",
            json={"token": token},
            headers={"Authorization": "Bearer invalid_token"},
        )
    assert response.status_code == 401


async def test_disconnect_user_with_invalid_authorization(app, token):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post(
            "/login/logout/",
            json={"token": token},
            headers={"Authorization": "Basic invalid_key"},
        )
    assert response.status_code == 401


async def test_disconnect_user_not_logged_in(app):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post(
            "/login/logout/",
            json={"token": "not_logged_in"},
            headers={"Authorization": "Bearer invalid_key"},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}


async def test_disconnect_user(app, token):
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        response = await ac.post(
            "/login/logout/",
            json={"token": token},
            headers={"Authorization": "Bearer invalid_key"},
        )
    assert response.status_code == 200
    assert response.json() == {"detail": "Player disconnected"}
