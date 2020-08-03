import asyncio

from aiogram import Bot, Dispatcher, executor
from ConfigBot import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    from Handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)