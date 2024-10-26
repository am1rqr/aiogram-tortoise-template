from aiogram import Router


def setup_routers() -> Router:
    from .users import (
        start
    )
    from .admins import (
        admin_panel
    )
    router = Router()
    router.include_routers(
        start.router,
        admin_panel.router
    )

    return router