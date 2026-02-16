import asyncio
import os
import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Импортируем роутер с обработчиками из модуля bot_logik.hendlers
from bot_logik.hendlers import handlers_router

# Создаём папку для логов, если её нет
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Настройка корневого логгера
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Консольный вывод
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Файловый вывод с ротацией
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "bot.log"),
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Логгер для этого модуля (остальные модули используют свои __name__)
main_logger = logging.getLogger(__name__)

load_dotenv()

async def start():
    """
        Главная асинхронная функция запуска бота.
        Создаёт экземпляр бота, диспетчер, подключает роутер и запускает polling.
        В случае ошибки логирует исключение, затем закрывает сессию бота.
        """
    # Создаём экземпляр бота с токеном из переменной окружения
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    # Создаём диспетчер
    dp = Dispatcher()
    # Подключаем роутер с обработчиками команд и колбэков
    dp.include_router(handlers_router)

    main_logger.info("Бот запущен и начинает polling")
    try:
        # Запускаем бесконечный цикл получения обновлений от Telegram
        await dp.start_polling(bot)
    except Exception as e:
        # Логируем любую ошибку с трассировкой
        main_logger.exception("Произошла ошибка во время polling: %s", e)
    finally:
        # Закрываем сессию бота (освобождаем ресурсы)
        await bot.session.close()
        main_logger.info("Сессия бота закрыта")

if __name__ == '__main__':
    # Точка входа: запускаем асинхронную функцию start
    asyncio.run(start())