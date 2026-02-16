import os
import logging

# Настраиваем логгер для этого модуля
logger = logging.getLogger(__name__)

async def check_subscription(user_id: int, bot) -> bool:
    """
    Проверяет, подписан ли пользователь на указанный канал.
    :param user_id: ID пользователя Telegram
    :param bot: экземпляр бота (aiogram.Bot), через который выполняется запрос
    :return: True, если пользователь является участником, администратором или создателем канала, иначе False
    """
    logger.debug("Проверка подписки для пользователя %s", user_id)
    try:
        # Получаем ID канала из переменной окружения
        chat_id = os.getenv("CHANNEL_ID")
        # Запрашиваем информацию о пользователе в канале
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        # Проверяем статус: "member" (участник), "administrator" (админ), "creator" (создатель)
        is_subscribed = member.status in ["member", "administrator", "creator"]
        logger.info("Пользователь %s подписан: %s", user_id, is_subscribed)
        return is_subscribed
    except Exception as e:
        # Логируем ошибку (например, бот не админ канала, канал не существует и т.п.)
        logger.error("Ошибка при проверке подписки для пользователя %s: %s", user_id, e, exc_info=True)
        # В случае любой ошибки считаем, что пользователь не подписан (безопасное поведение)
        return False