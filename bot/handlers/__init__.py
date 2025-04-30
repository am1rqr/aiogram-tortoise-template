from aiogram import Router


def setup_routers() -> Router:
    from .users import (
        start
    )
    from .admins import (
        admin_panel,
        mailing,
        bot_stats,
        find_user
    )
    from .admins.ad_links import routers as ad_links_routers

    router = Router()
    router.include_routers(
        start.router,

        admin_panel.router,
        mailing.router,
        bot_stats.router,
        find_user.router,
        *ad_links_routers
    )

    return router