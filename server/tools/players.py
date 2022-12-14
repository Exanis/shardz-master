"""
This module manage the players connection to the master server.
It will handle managing the player's sessions in the server.
"""
from typing import List, Dict, Optional
from secrets import token_hex
from fastapi import HTTPException, Depends
from .authorization import authorization_key


PLAYERS: Dict[str, str] = {}
CONNECTED_PLAYERS: List[str] = []


def try_login_player(player_id: str) -> Optional[str]:
    """
    Try to login a player. If the player is already logged in, returns None.
    Otherwise, creates a new session for the player and returns the session id.

    The session ID is a random ID safe for the player to know ; it is not a static
    number linked to the user's identity.

    :param player_id: The player id to login
    :return: The session id if the player is logged in, None otherwise
    """
    if player_id in CONNECTED_PLAYERS:
        return None
    CONNECTED_PLAYERS.append(player_id)
    token = token_hex(255)
    PLAYERS[token] = player_id
    return token


def disconnect_player(player_token: str) -> bool:
    """
    Disconnect a player from the server.

    :param player_token: The player's session id (as provided by try_login_player)
    :return: True if the player was disconnected, False otherwise
    """
    if player_token in PLAYERS:
        CONNECTED_PLAYERS.remove(PLAYERS[player_token])
        del PLAYERS[player_token]
        return True
    return False


def require_user(token: str = Depends(authorization_key)) -> str:
    """
    Dependency to require an user to be logged in.

    :param token: The authorization key (automatically injected)
    :return: The player id
    :raises HTTPException: 401 If the token is invalid.
    """
    if token not in PLAYERS:
        raise HTTPException(status_code=401, detail="Invalid token")
    return PLAYERS[token]
