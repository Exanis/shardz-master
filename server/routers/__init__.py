"""
Routers used by the server
"""
__all__ = ["authentication_router", "servers_router"]


from .authentication import router as authentication_router
from .servers import router as servers_router
