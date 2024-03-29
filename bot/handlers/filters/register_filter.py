from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.methods import SendMessage

from sqlalchemy.orm import sessionmaker

from bot.db import is_user_exists
from bot.handlers.keyboards.worker_kb import START_WORKER_BOARD


class IsRegisterFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(
            self,
            message: Message,
            session_maker: sessionmaker) -> bool:
        if not await is_user_exists(int(message.from_user.id), session_maker):
            await SendMessage(
                text='Доступно только зарегистрированному пользователю',
                chat_id=message.from_user.id,
                reply_markup=START_WORKER_BOARD
            )
            return False
        return message.text == self.my_text
