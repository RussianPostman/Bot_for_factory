# import os
# import asyncio
# import logging
# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv

# from ..bot.handlers import register_router

# # from bot.handlers import register_router 

# load_dotenv()


# TELEGRAM_TOKEN = os.getenv('TOKEN')

# async def main():
#     logging.basicConfig(level=logging.DEBUG)

#     dp = Dispatcher
#     bot = Bot(TELEGRAM_TOKEN)

#     register_router(dp)

#     await dp.start_polling(bot)


# if __name__ == '__main__':
#     asyncio.run(main())
