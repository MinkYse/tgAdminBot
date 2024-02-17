import asyncio

from django.core.management.base import BaseCommand

from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import router
from bot.admin_handler import admin_router
from bot.handlers_client import client_router


bot = Bot(token='6644534760:AAGNW1Wkjw5kw9fDjn68WdHZAvYKj50sPWM', parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)
dp.include_router(admin_router)
dp.include_router(client_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# if __name__ == "__main__":
class Command(BaseCommand):
    asyncio.run(main())
