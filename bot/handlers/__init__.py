from aiogram import Router


def setup_routers() -> Router:
    from .users import (
        start
    )
    from .admins import (
        admin_panel,
        mailing,
        bot_stats
    )
    router = Router()
    router.include_routers(
        start.router,
        admin_panel.router,
        mailing.router,
        bot_stats.router
    )

    return router