from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.builders import back_to_builder, find_user_builder
from bot.keyboards.reply import find_user_kb
from bot.states.admins import FindUser, ChangeUserNote, SendUserMessage
from database.commands.user import select_user_by_id, select_user_by_username, change_user_status, update_user_note
from database.models import Users

router = Router()


async def format_user_info(user: Users) -> tuple[str, str, str, str, str]:
    user_info = f"@{user.username} | {user.user_id}" if user.username else f"{user.first_name} | ID {user.user_id}"
    note = user.note if user.note else "-"
    user_status = "Активен" if user.status == "active" else "Заблокирован"
    registration_date = user.created_at.strftime('%d.%m.%Y %H:%M:%S')
    last_activity = user.last_activity.strftime('%d.%m.%Y %H:%M:%S')

    return user_info, note, user_status, registration_date, last_activity


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

    user_info, note, user_status, registration_date, last_activity = await format_user_info(user)
    await message.answer(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>📝 Заметка: <i>{note}</i></b>\n"
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

    user_info, note, user_status, registration_date, last_activity = await format_user_info(user)
    await message.answer(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>📝 Заметка: <i>{note}</i></b>\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> UTC.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> UTC.</b>",
        reply_markup=find_user_builder(user.status, user.user_id)
    )
    await state.clear()


@router.callback_query(F.data.startswith("change_user_status#"))
async def call_change_user_status(call: CallbackQuery):
    user_id = int(call.data.split("#")[1])
    user = await select_user_by_id(user_id)

    user_info, note, user_status, registration_date, last_activity = await format_user_info(user)

    user_status = "Заблокирован" if user.status == "active" else "Активен"
    user_kb_status = "blocked" if user.status == "active" else "active"

    await call.message.edit_text(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>📝 Заметка: <i>{note}</i></b>\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> UTC.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> UTC.</b>",
        reply_markup=find_user_builder(user_kb_status, user.user_id)
    )
    await change_user_status(user_id)
    await call.answer("✅ Статус пользователя успешно изменен.", show_alert=True)


@router.callback_query(F.data.startswith("call_find_user#"))
async def call_find_user(call: CallbackQuery, state: FSMContext) -> None:
    user_id = int(call.data.split("#")[1])
    user = await select_user_by_id(user_id)

    user_info, note, user_status, registration_date, last_activity = await format_user_info(user)
    await call.message.edit_text(
        f"<b>👤 Пользователь {user_info}</b>\n\n"
        f"<b>📝 Заметка: <i>{note}</i></b>\n"
        f"<b>⭐️ Статус: <i>{user_status}</i></b>\n\n"
        f"<b>🔔 Последняя активность: <i>{last_activity}</i> UTC.</b>\n"
        f"<b>📅 Зарегистрирован: <i>{registration_date}</i> UTC.</b>",
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

    await update_user_note(user_id, message.text)

    await message.answer("<b>✅ Заметка успешно изменена.</b>",
                         reply_markup=back_to_builder(f"call_find_user#{user_id}"))
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
    except TelegramAPIError:
        await message.answer("<b>❌ Не удалось отправить сообщение.</b>",
                             reply_markup=back_to_builder(f"call_find_user#{user_id}"))
        return

    await message.answer("<b>✅ Сообщение успешно отправлено.</b>",
                         reply_markup=back_to_builder(f"call_find_user#{user_id}"))
    await state.clear()