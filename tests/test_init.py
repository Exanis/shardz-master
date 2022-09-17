import pytest
from server.settings import settings
from server.main import startup


async def test_startup_with_invalid_key():
    initial_debug = settings.debug
    initial_key = settings.api_key
    settings.debug = False
    settings.api_key = "invalid_key"
    with pytest.raises(RuntimeError):
        await startup()
    settings.debug = initial_debug
    settings.api_key = initial_key


async def test_startup_with_valid_key():
    initial_debug = settings.debug
    initial_key = settings.api_key
    settings.debug = False
    settings.api_key = "valid_key"
    await startup()
    settings.debug = initial_debug
    settings.api_key = initial_key
