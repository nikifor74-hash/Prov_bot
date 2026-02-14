import os

from aiogram import Router, types, Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv

from bot_logik.chec_pr import check_subscription

dp = Dispatcher()
load_dotenv()

handlers_router=Router()
CHANNEL_ID=os.getenv("CHANNEL_ID")

@handlers_router.message(Command("start"))
async def start_command(message: types.Message):
    if await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Скачать файл", url=os.getenv("FILE_LINK"))]
        ])
        await message.answer("✅ Доступ открыт!", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
                InlineKeyboardButton(text="Проверить подписку", callback_data="check")
            ]
        ])
        await message.answer("Подпишитесь на канал для доступа:", reply_markup=keyboard)

@handlers_router.callback_query(lambda c: c.data == "check")
async def check_callback(callback: types.CallbackQuery):
    if await check_subscription(callback.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Скачать файл", url=os.getenv("FILE_LINK"))]
        ])
        await callback.message.edit_text("✅ Доступ открыт!", reply_markup=keyboard)
    else:
        await callback.answer("❌ Вы еще не подписались!", show_alert=True)