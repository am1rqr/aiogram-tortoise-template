from database.models import Users


async def select_user_by_id(user_id: int) -> Users:
    user = await Users.filter(user_id=user_id).first()
    return user