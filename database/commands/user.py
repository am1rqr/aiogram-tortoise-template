from datetime import datetime, timedelta, UTC

from pydantic.v1.validators import anystr_strip_whitespace
from tortoise.expressions import Case, When, Value

from database.enums import UserStatus
from database.models import Users


async def create_user(user_id: int, username: str, first_name: str, language_code: str) -> Users:
    return await Users.create(user_id=user_id,
                              username=username,
                              first_name=first_name,
                              language_code=language_code)


async def select_user_by_id(user_id: int) -> Users | None:
    return await Users.get_or_none(user_id=user_id)


async def select_user_by_username(username: str) -> Users | None:
    return await Users.get_or_none(username=username)


async def all_time_count_users() -> int:
    return await Users.all().count()


async def timely_count_users(days: int) -> int:
    start_date = datetime.now() - timedelta(days=days)
    return await Users.filter(created_at__gte=start_date).count()


async def get_all_users() -> list[Users]:
    return await Users.all()


async def change_user_status(user_id: int) -> None:
    await Users.filter(user_id=user_id).update(
        status=Case(
            When(status=UserStatus.ACTIVE, then=Value(UserStatus.BANNED)),
            default=Value(UserStatus.ACTIVE)
        )
    )


async def update_user_last_activity(user_id: int) -> None:
    await Users.filter(user_id=user_id).update(last_activity=datetime.now(UTC))


async def update_user_username(user_id: int, username: str) -> None:
    await Users.filter(user_id=user_id).update(username=username)


async def update_user_note(user_id: int, note: str) -> None:
    await Users.filter(user_id=user_id).update(note=note)