from database.models import Users


async def select_user_by_id(user_id: int) -> Users:
    user = await Users.filter(user_id=user_id).first()
    return user


async def count_users() -> int:
    users_count = await Users.all().count()
    return users_count


async def get_all_users() -> list[Users]:
    users = await Users.all()
    return users