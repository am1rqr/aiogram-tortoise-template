from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.builder import back_to_builder
from bot.states.admins import Mailing
from database import commands
from main import bot

router = Router()


@router.callback_query(F.data == "mailing")
async def mailing(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text("Send a newsletter to all users:",
                                 reply_markup=back_to_builder("admin_panel"))
    await state.set_state(Mailing.media)


@router.message(Mailing.media)
async def get_mailing_media(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.html_text)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Approval", callback_data="approval_mailing")
        ],
        [
            InlineKeyboardButton(text="Cancel", callback_data="admin_panel")
        ]
    ])
    if message.photo:
        photo = message.photo[-1]
        await state.update_data(photo=photo.file_id)

        await message.answer("Are you sure you want to start sending out a newsletter with this photo and text?",
                             reply_markup=markup)
    else:
        await message.answer(f"Do you really want to start a mailing with the text:\n\n"
                             f"{message.html_text}",
                             disable_web_page_preview=True,
                             reply_markup=markup)


@router.callback_query(F.data == "approval_mailing")
async def approval_mailing(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get("text")
    photo = data.get("photo")

    await call.message.edit_text("Mailing in progress...")

    users = await commands.get_all_users()
    for user in users:
        try:
            if photo:
                await bot.send_photo(chat_id=user.user_id,
                                     photo=photo,
                                     caption=text)
            else:
                await bot.send_message(chat_id=user.user_id,
                                       text=text)
        except Exception as e:
            print(e)

    await call.message.answer("Mailing completed successfully")
    await state.clear()