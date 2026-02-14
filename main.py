import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot_logik.hendlers import handlers_router

load_dotenv()

async def start():
    bot=Bot(token=os.getenv("BOT_TOKEN"))
    dp=Dispatcher()

    dp.include_router(handlers_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())