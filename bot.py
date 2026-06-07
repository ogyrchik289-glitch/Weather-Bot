from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from handlers.handlers import handler_router
load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

dp = Dispatcher()

dp.include_router(handler_router)

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    