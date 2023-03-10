from aiogram import types

from bot.handlers.keyboards.admin_kb import GOOGLE_SHEETS_LINK


async def tables_list(
        message: types.Message,
        ):
    await message.answer(
        'Выберите таблицу',
        reply_markup=GOOGLE_SHEETS_LINK
        )
