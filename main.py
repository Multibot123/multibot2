from modules import ai_chat, alerts, archive, payments, referral, rent
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from db.database import init_db
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    alerts.bot = bot
    dp = Dispatcher()
    ai_chat.register_handlers(dp)
    alerts.register_handlers(dp)
    archive.register_handlers(dp)
    payments.register_handlers(dp)
    referral.register_handlers(dp)
    rent.register_handlers(dp)

    # Запуск планировщика авторассылки
    loop = asyncio.get_running_loop()
    loop.create_task(alerts.rent_alert_scheduler())

    await dp.start_polling(bot)

if __name__ == "__main__":
    init_db()
    asyncio.run(main())