from database.models import AdLinks


async def get_all_links() -> list[AdLinks]:
    return await AdLinks.all()