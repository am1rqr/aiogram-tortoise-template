from datetime import datetime, timedelta, UTC

from database.models import Users


async def select_user_by_id(user_id: int) -> Users:
    user = await Users.filter(user_id=user_id).first()
    return user


async def select_user_by_username(username: str) -> Users:
    user = await Users.filter(username=username).first()
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


async def change_user_status(user_id: int) -> None:
    user = await select_user_by_id(user_id)
    if user.status == "active":
        await Users.filter(user_id=user_id).update(status="banned")
    else:
        await Users.filter(user_id=user_id).update(status="active")


async def update_user_last_activity(user_id: int) -> None:
    await Users.filter(user_id=user_id).update(last_activity=datetime.now(UTC))


async def update_user_username(user_id: int, username: str) -> None:
    await Users.filter(user_id=user_id).update(username=username)


async def update_user_note(user_id: int, note: str) -> None:
    await Users.filter(user_id=user_id).update(note=note)