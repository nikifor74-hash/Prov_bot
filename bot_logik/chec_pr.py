import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()
bot=Bot(token=os.getenv("BOT_TOKEN"))

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=os.getenv("CHANNEL_ID"), user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False