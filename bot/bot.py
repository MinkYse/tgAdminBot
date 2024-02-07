import asyncio
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from django.core.management import call_command

from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router


bot = Bot(token='6644534760:AAGNW1Wkjw5kw9fDjn68WdHZAvYKj50sPWM', parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
