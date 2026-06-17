from Storage_logic_v2.SQLite_logic import SQLiteDB
from Business_logic.Business_logic import BusinessLogic
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from UI_tg_bot.Handlers.start_handler import router
from UI_tg_bot.Handlers.dates_handler import date_router
from UI_tg_bot.Handlers.notes_handler import note_router
from UI_tg_bot.Cache.User_cache import UserCache
from UI_tg_bot.Middlewares.AuthMiddleware import AuthMiddleware
import asyncio


async def main():
    storage = SQLiteDB()
    logic = BusinessLogic(storage)
    cache = UserCache()

    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp["logic"] = logic
    dp["cache"] = cache
    dp.include_router(router)
    dp.include_router(date_router)
    dp.include_router(note_router)
    dp.message.middleware(AuthMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())