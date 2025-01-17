from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.builders import back_to_builder, find_user_builder
from bot.keyboards.reply import find_user_kb
from bot.states.admins import FindUser
from database.commands.user import select_user_by_id, select_user_by_username, change_user_status
from database.models import Users

router = Router()


async def format_user_info(user: Users) -> tuple[str, str, str, str]:
    user_info = f"@{user.username} | {user.user_id}" if user.username else f"{user.first_name} | ID {user.user_id}"
    user_status = "Активен" if user.status == "active" else "Заблокирован"
    registration_date = user.created_at.strftime('%d.%m.%Y %H:%M:%S')
    last_activity = user.last_activity.strftime('%d.%m.%Y %H:%M:%S')
    return user_info, user_status, registration_date, last_activity


@router.callback_query(F.data == "find_user")
async def call_find_user(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()

    await call.message.answer(
        "<b>✍️ Введите ID, username или нажмите на кнопку чтобы найти пользователя.</b>",
        reply_markup=find_user_kb
    )
    await state.set_state(FindUser.user)


@router.message(F.user_shared, FindUser.user)
async def get_user_shared(message: Message, state: FSMContext):
    user = await select_user_by_id(message.user_shared.user_id)
    if not user:
        await message.answer(
            "<i>❌ Пользователь не найден.</i>",
            reply_markup=back_to_builder("admin_panel")
        )
        return

    user_info, user_status, registration_date, last_activity = await format_user_info(user)
    await message.answer(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> UTC.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> UTC.</b>",
        reply_markup=find_user_builder(user.status, user.user_id)
    )
    await state.clear()


@router.message(FindUser.user)
async def get_user(message: Message, state: FSMContext):
    text = message.text.strip("@")
    user = await (select_user_by_id(int(text)) if text.isdigit() else select_user_by_username(text))

    if not user:
        await message.answer(
            "<i>❌ Некорректный ID или username. Попробуйте еще раз.</i>",
            reply_markup=back_to_builder("admin_panel")
        )
        return

    user_info, user_status, registration_date, last_activity = await format_user_info(user)
    await message.answer(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> UTC.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> UTC.</b>",
        reply_markup=find_user_builder(user.status, user.user_id)
    )
    await state.clear()


@router.callback_query(F.data.startswith("change_user_status#"))
async def call_change_user_status(call: CallbackQuery):
    user_id = int(call.data.split("#")[1])
    user = await select_user_by_id(user_id)

    user_info, user_status, registration_date, last_activity = await format_user_info(user)
    user_kb_status = "blocked" if user.status == "active" else "active"

    await call.message.edit_text(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> UTC.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> UTC.</b>",
        reply_markup=find_user_builder(user_kb_status, user.user_id)
    )
    await change_user_status(user_id)
    await call.answer("✅ Статус пользователя успешно изменен.", show_alert=True)
