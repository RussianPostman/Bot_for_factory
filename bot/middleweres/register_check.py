from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from sqlalchemy.orm import sessionmaker

from bot.db import is_user_exists


class RegisterCheck(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        session_maker: sessionmaker = data['session_maker']

        if not await is_user_exists(user_id, session_maker):
            await data['bot'].send_message(
                event.from_user.id,
                'Ты не зарегистрирован!'
            )

        return await handler(event, data)
