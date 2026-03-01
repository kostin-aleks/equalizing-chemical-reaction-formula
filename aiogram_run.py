import asyncio

from create_bot import bot, dp  # , scheduler
from handlers.admin_panel import admin_router
from handlers.start import set_commands, start_router

# from work_time.time_func import send_time_msg


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    dp.include_router(admin_router)
    dp.include_router(start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    asyncio.run(main())
