from os import environ
from typing import List
import pytest
from fastapi import FastAPI
from pytest_httpx import HTTPXMock


environ.setdefault("DEBUG", "True")


# pytest-httpx configuration
@pytest.fixture
def assert_all_responses_were_requested() -> bool:
    """We don't want every responses to be requested as we are setting up everything in most tests"""
    return False


@pytest.fixture
def non_mocked_hosts() -> List[str]:
    """
    Requests against http://test are requests against our own API (ie the one we want to test)
    so we are not mocking them.
    """
    return ["test"]


@pytest.fixture
def httpx(httpx_mock: HTTPXMock) -> HTTPXMock:
    """Pre-set basic responses to httpx since we are going to need them"""
    httpx_mock.add_response(
        url="http://identification/login/",
        match_content=b'{"credentials": "valid"}',
        status_code=200,
        json={"identifier": "valid_user_identifier"},
    )
    httpx_mock.add_response(
        url="http://identification/login/",
        match_content=b'{"credentials": "invalid"}',
        status_code=401,
    )
    return httpx_mock


# Servers fixtures
def get_app() -> FastAPI:
    """Returns the FastAPI app we want to test"""
    from server.main import app

    return app


@pytest.fixture
def app(httpx: HTTPXMock) -> FastAPI:
    httpx.add_response(url="http://servers/list/", status_code=200, json=[])
    return get_app()


@pytest.fixture
def app_with_servers(httpx: HTTPXMock) -> FastAPI:
    httpx.add_response(
        url="http://servers/list/",
        status_code=200,
        json=[
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
        ],
    )
    return get_app()


# Connection fixtures
@pytest.fixture
def token() -> str:
    from server.tools.players import PLAYERS, try_login_player

    try_login_player("valid_user_identifier")
    return list(PLAYERS.keys())[0]
