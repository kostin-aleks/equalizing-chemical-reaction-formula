import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Импортируем роутеры из файлов
from handlers import basic_handlers, menu_handlers, start

load_dotenv()

BOT_TOKEN = os.environ["TOKEN_BOT"]

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()

# Запуск процесса поллинга новых апдейтов


async def main():
    # Регистрируем роутер в диспетчере
    dp.include_router(menu_handlers.router)
    dp.include_router(start.start_router)
    dp.include_router(basic_handlers.router)

    # Удаляем вебхук и пропускаем накопившиеся входящие сообщения
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
