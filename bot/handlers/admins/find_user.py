from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.builders import back_to_builder, find_user_builder
from bot.states.admins import FindUser
from database.commands.user import select_user_by_id, select_user_by_username, change_user_status

router = Router()


@router.callback_query(F.data == "find_user")
async def call_find_user(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text("<b>✍️ Введите ID или username пользователя, которого хотите найти.</b>",
                                 reply_markup=back_to_builder("admin_panel"))
    await state.set_state(FindUser.user)


@router.message(FindUser.user)
async def get_user(message: Message, state: FSMContext) -> None:
    text = message.text
    if text.isdigit():
        user = await select_user_by_id(int(text))
    elif isinstance(text, str):
        if text.startswith("@"):
            text = text[1:]
        user = await select_user_by_username(text)
    else:
        await message.answer("<i>❌ Некорректный ID или username. Попробуйте еще раз.</i>",
                             reply_markup=back_to_builder("admin_panel"))
        return

    if not user:
        await message.answer("<i>❌ Пользователь не найден.</i>")
        return

    user_info = f"@{user.username} | {user.user_id}"
    if not user.username:
        user_info = f"ID {user.user_id}"

    user_status = "Активен" if user.status == "active" else "Заблокирован"

    await message.answer(f"<b>👤 Пользователь {user_info}</b>\n\n"
                         f"<b>⭐️ Статус: <i>{user_status}</i></b>\n"
                         f"<b>📅 Зарегистрирован: <i>{user.created_at.strftime('%d.%m.%Y %H:%M:%S')}</i> UTC.</b>",
                         reply_markup=find_user_builder(user.status, user.user_id))


@router.callback_query(F.data.startswith("change_user_status#"))
async def call_change_user_status(call: CallbackQuery) -> None:
    user_id = int(call.data.split("#")[1])
    user = await select_user_by_id(user_id)

    user_info = f"@{user.username} | {user.user_id}"
    if not user.username:
        user_info = f"ID {user.user_id}"

    user_status = "Заблокирован" if user.status == "active" else "Активен"
    user_kb_status = "blocked" if user.status == "active" else "active"

    await call.message.edit_text(f"<b>👤 Пользователь {user_info}</b>\n\n"
                                 f"<b>⭐️ Статус: <i>{user_status}</i></b>\n"
                                 f"<b>📅 Зарегистрирован: <i>{user.created_at.strftime('%d.%m.%Y %H:%M:%S')}</i> UTC.</b>",
                                 reply_markup=find_user_builder(user_kb_status, user.user_id))

    await change_user_status(user_id)
    await call.answer("✅ Статус пользователя успешно изменен.",
                      show_alert=True)