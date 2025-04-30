from .create import router as create_router
from .view import router as view_router
from .delete import router as delete_router

routers = [create_router, view_router, delete_router]
