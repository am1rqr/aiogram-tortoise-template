from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.builders import back_to_builder, find_user_builder
from bot.states.admins import FindUser, ChangeUserNote, SendUserMessage
from config import TZ_INFO
from database.commands.user import select_user_by_id, select_user_by_username, change_user_status, update_user_note
from database.enums import UserStatus
from database.models import Users
from config import tz

router = Router()


def format_user_info(user: Users) -> tuple[str, str, str, str, str]:
    user_info = f"@{user.username} | {user.user_id}" if user.username else f"{user.first_name} | ID {user.user_id}"
    note = user.note if user.note else "-"
    user_status = "Активен" if user.status == "active" else "Заблокирован"
    registration_date = user.created_at.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")
    last_activity = user.last_activity.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")

    return user_info, note, user_status, registration_date, last_activity


def get_user_info_text(user_info, note, user_status, registration_date, last_activity) -> str:
    user_info = (
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>📝 Заметка: <i>{note}</i></b>\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> {TZ_INFO}.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> {TZ_INFO}.</b>"
    )
    return user_info


@router.callback_query(F.data == "find_user")
async def call_find_user(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()

    await call.message.edit_text(
        "<b>✍️ Введите ID или username пользователя:</b>",
        reply_markup=back_to_builder("admin_panel")
    )
    await state.set_state(FindUser.user)


@router.message(FindUser.user)
async def get_user(message: Message, state: FSMContext):
    text = message.text.strip("@")
    user = await (select_user_by_id(int(text)) if text.isdigit() else select_user_by_username(text))

    if not user:
        await message.answer(
            "<i>❌ Некорректный ID или username. Попробуйте еще раз:</i>",
            reply_markup=back_to_builder("admin_panel")
        )
        return

    user_info = format_user_info(user)
    user_info_text = get_user_info_text(*user_info)

    await message.answer(
        user_info_text,
        reply_markup=find_user_builder(user.status, user.user_id)
    )
    await state.clear()


@router.callback_query(F.data.startswith("change_user_status#"))
async def call_change_user_status(call: CallbackQuery):
    user_id = int(call.data.split("#")[1])
    user = await select_user_by_id(user_id)

    user_status = "Заблокирован" if user.status == UserStatus.ACTIVE else "Активен"
    user_kb_status = "blocked" if user.status == UserStatus.ACTIVE else "active"

    user_info = format_user_info(user)
    user_info_text = get_user_info_text(*user_info)

    await call.message.edit_text(
        user_info_text,
        reply_markup=find_user_builder(user_kb_status, user.user_id)
    )
    await change_user_status(user_id)
    await call.answer("✅ Статус пользователя успешно изменен.", show_alert=True)


@router.callback_query(F.data.startswith("call_find_user#"))
async def call_find_user(call: CallbackQuery, state: FSMContext) -> None:
    user_id = int(call.data.split("#")[1])
    user = await select_user_by_id(user_id)

    user_info = format_user_info(user)
    user_info_text = get_user_info_text(*user_info)
    await call.message.edit_text(
        user_info_text,
        reply_markup=find_user_builder(user.status, user.user_id)
    )
    await state.clear()


@router.callback_query(F.data.startswith("change_user_note#"))
async def call_change_user_note(call: CallbackQuery, state: FSMContext) -> None:
    user_id = int(call.data.split("#")[1])
    await state.update_data(user_id=user_id)

    await call.message.edit_text(
        "<b>✍️ Введите новую заметку для пользователя.</b>",
        reply_markup=back_to_builder(f"call_find_user#{user_id}")
    )
    await state.set_state(ChangeUserNote.note)


@router.message(F.text, ChangeUserNote.note)
async def get_new_user_note(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user_id: int = data.get("user_id")

    user = await select_user_by_id(user_id)
    user_info, note, user_status, registration_date, last_activity = format_user_info(user)

    note = message.text
    user_info_text = get_user_info_text(user_info, note, user_status, registration_date, last_activity)

    await message.answer(
        user_info_text,
        reply_markup=find_user_builder(user.status, user.user_id)
    )

    await update_user_note(user_id, message.text)
    await state.clear()


@router.callback_query(F.data.startswith("send_message#"))
async def call_send_user_message(call: CallbackQuery, state: FSMContext) -> None:
    user_id = int(call.data.split("#")[1])
    await state.update_data(user_id=user_id)

    await call.message.edit_text(
        "<b>✍️ Введите сообщение для пользователя.</b>",
        reply_markup=back_to_builder(f"call_find_user#{user_id}")
    )
    await state.set_state(SendUserMessage.message)


@router.message(F.text, SendUserMessage.message)
async def get_user_message(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    user_id: int = data.get("user_id")

    try:
        await bot.send_message(user_id, message.html_text)

        await message.answer("<b><i>✅ Сообщение успешно отправлено.</i></b>")
    except TelegramAPIError:
        await message.answer("<b><i>❌ Не удалось отправить сообщение.</i></b>")

    user = await select_user_by_id(user_id)
    user_info = format_user_info(user)
    user_info_text = get_user_info_text(*user_info)

    await message.answer(
        user_info_text,
        reply_markup=find_user_builder(user.status, user.user_id)
    )
    await state.clear()