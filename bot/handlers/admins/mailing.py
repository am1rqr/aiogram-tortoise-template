from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.builders import back_to_builder, approval_builder, button_builder
from bot.states.admins import Mailing
from database.commands.user import get_all_users
from main import bot

router = Router()


@router.callback_query(F.data == "mailing")
async def mailing(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text("<b>📝 Пришлите рассылку которую хотите отправить всем пользователям:</b>",
                                 reply_markup=back_to_builder("admin_panel"))
    await state.set_state(Mailing.media)


@router.message(Mailing.media)
async def get_mailing_media(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.html_text)
    if message.photo:
        photo = message.photo[-1]
        await state.update_data(photo=photo.file_id)

    await message.answer("<b>⌨️ Если хотите добавить клавиатуру отправьте в формате <i>Текст кнопки::Ссылка</i></b>",
                         reply_markup=button_builder("❌Пропустить", "approval_mailing"))
    await state.set_state(Mailing.keyboard)


@router.message(Mailing.keyboard)
async def get_mailing_keyboard(message: Message, state: FSMContext) -> None:
    if "::" not in message.text or message.text.count("::") > 1:
        await message.answer("<b>🚫 Неверный формат клавиатуры, попробуйте еще раз:</b>",
                             reply_markup=back_to_builder("mailing"))
        return

    keyboard = message.text.split("::")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=keyboard[0], url=keyboard[1])]
    ])
    await state.update_data(markup=markup)

    data = await state.get_data()
    text: str = data.get("text")
    photo: str = data.get("photo")

    if photo:
        await message.answer_photo(photo=photo,
                                   caption=text,
                                   reply_markup=markup)
    else:
        await message.answer(text,
                             reply_markup=markup)

    await message.answer("<b>❓ Вы уверены что хотите начать рассылку?</b>",
                         reply_markup=approval_builder("approval_mailing", "mailing"))


@router.callback_query(F.data == "approval_mailing")
async def approval_mailing(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text: str = data.get("text")
    photo: str = data.get("photo")
    markup: InlineKeyboardMarkup | None = data.get("markup")

    await call.message.edit_text("<i>🔄 Рассылка в процессе...</i>")

    not_delivered_count = 0

    users = await get_all_users()
    for user in users:
        try:
            if photo:
                await bot.send_photo(chat_id=user.user_id,
                                     photo=photo,
                                     caption=text,
                                     reply_markup=markup)
            else:
                await bot.send_message(chat_id=user.user_id,
                                       text=text,
                                       reply_markup=markup)
        except TelegramAPIError:
            not_delivered_count += 1

    delivered_count = len(users) - not_delivered_count

    await call.message.answer(f"<b>✅ Рассылка успешно завершена!</b>\n\n"
                              f"<b>📨 Отправлено: <i>{delivered_count}</i></b>\n"
                              f"<b>❗️Не доставлено: <i>{not_delivered_count}</i></b>",
                              reply_markup=back_to_builder("admin_panel"))
    await state.clear()
