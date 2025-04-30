from database.enums import AdLinkStatus
from database.models import AdLinks


async def get_all_active_ad_links() -> list[AdLinks]:
    return await AdLinks.filter(status=AdLinkStatus.ACTIVE).all()


async def get_ad_link_by_code(code: str) -> AdLinks:
    return await AdLinks.get_or_none(code=code)


async def add_ad_link(title: str, code: str) -> None:
    await AdLinks.create(title=title, code=code)


async def get_ad_link_by_id(ad_link_id: int) -> AdLinks:
    return await AdLinks.get_or_none(id=ad_link_id)


async def delete_ad_link(ad_link_id: int) -> None:
    await AdLinks.filter(id=ad_link_id).update(status=AdLinkStatus.DELETED)
