from database.models import AdLinks


async def get_all_links() -> list[AdLinks]:
    return await AdLinks.all()


async def get_ad_link_by_code(code: str) -> AdLinks:
    return await AdLinks.get_or_none(code=code)


async def add_ad_link(title: str, code: str) -> None:
    await AdLinks.create(title=title, code=code)