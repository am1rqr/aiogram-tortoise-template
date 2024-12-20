from datetime import datetime, timedelta

from database.models import Users


async def select_user_by_id(user_id: int) -> Users:
    user = await Users.filter(user_id=user_id).first()
    return user


async def all_time_count_users() -> int:
    count = await Users.all().count()
    return count


async def timely_count_users(days: int) -> int:
    start_date = datetime.now() - timedelta(days=days)
    count = await Users.filter(created_at__gte=start_date).count()
    return count


async def get_all_users() -> list[Users]:
    users = await Users.all()
    return users