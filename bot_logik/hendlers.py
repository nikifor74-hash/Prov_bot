import os
import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Импортируем функцию проверки подписки из соседнего модуля
from bot_logik.chec_pr import check_subscription

# Настраиваем логгер для этого модуля
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Создаём роутер, на который будем вешать обработчики
handlers_router = Router()

# Получаем ID канала из .env (может быть в формате @channelusername или числовой ID)
CHANNEL_ID = os.getenv("CHANNEL_ID")

@handlers_router.message(Command("start"))
async def start_command(message: types.Message):
    """
        Обработчик команды /start.
        Проверяет, подписан ли пользователь на канал.
        Если подписан – выдаёт кнопку со ссылкой на файл.
        Если нет – предлагает подписаться и даёт кнопку проверки подписки.
        """
    user_id = message.from_user.id
    logger.info("Получена команда /start от пользователя %s", user_id)

    # Проверяем подписку, передаём ID пользователя и объект бота из сообщения
    if await check_subscription(user_id, message.bot):
        logger.info("Пользователь %s подписан, выдаём доступ", user_id)
        # Создаём клавиатуру с одной кнопкой для скачивания файла
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Скачать файл", url=os.getenv("FILE_LINK"))]
        ])
        await message.answer("✅ Доступ открыт!", reply_markup=keyboard)
    else:
        logger.info("Пользователь %s не подписан, предлагаем подписаться", user_id)
        # Клавиатура с двумя кнопками: подписаться (ссылка на канал) и проверить подписку (callbac
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
                InlineKeyboardButton(text="Проверить подписку", callback_data="check")
            ]
        ])
        await message.answer("Подпишитесь на канал для доступа:", reply_markup=keyboard)

@handlers_router.callback_query(lambda c: c.data == "check")
async def check_callback(callback: types.CallbackQuery):
    """
        Обработчик нажатия на кнопку "Проверить подписку" (callback_data = "check").
        Проверяет подписку пользователя.
        Если подписка подтверждена:
            - Если сообщение ещё не было изменено на "Доступ открыт!", обновляет его,
              заменяя клавиатуру на кнопку скачивания.
            - Если сообщение уже содержит этот текст, просто отвечает уведомлением,
              чтобы избежать ошибки "message is not modified".
        Если не подписан – показывает предупреждение.
        """
    user_id = callback.from_user.id
    logger.info("Получен callback 'check' от пользователя %s", user_id)
    # Проверяем подписку, передаём ID и объект бота из callback
    if await check_subscription(user_id, callback.bot):
        # Проверяем, не обновлено ли уже сообщение
        if callback.message.text == "✅ Доступ открыт!":
            logger.info("Пользователь %s уже имеет доступ, пропускаем редактирование", user_id)
            # Просто показываем всплывающее уведомление
            await callback.answer("✅ Доступ уже открыт!")
            return

        logger.info("Пользователь %s теперь подписан, обновляем сообщение", user_id)
        # Создаём клавиатуру с кнопкой скачивания файла
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Скачать файл", url=os.getenv("FILE_LINK"))]
        ])
        # Редактируем существующее сообщение, заменяя текст и клавиатуру
        await callback.message.edit_text("✅ Доступ открыт!", reply_markup=keyboard)
    else:
        logger.info("Пользователь %s всё ещё не подписан", user_id)
        # Показываем предупреждение с красным уведомлением (show_alert=True)
        await callback.answer("❌ Вы еще не подписались!", show_alert=True)
