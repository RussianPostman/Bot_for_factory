from datetime import datetime

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram import types

from sqlalchemy.orm import sessionmaker

from bot.db import get_сategory_list, get_products_list, get_user_roles, \
    User, Product, get_user, get_product, create_report
from bot.handlers.keyboards.worker_kb import generate_categorys_board, \
    generate_product_board, generate_roles_board, simple_generate_board
from bot.handlers.keyboards.worker_kb import CategoryCD, ProductCD, \
    UserRoleCD, SalarysCD
from bot.googlr_sheets.user_tools import add_reports, read_salarys
from bot.handlers.keyboards.worker_kb import START_WORKER_BOARD, \
    SELECT_TYPE_REPORT


ROLE_NAMES = {
    'Токарь': 'turner',
    'Литейщик': 'caster',
    'Фрезеровщик': 'miller',
    'Упаковщик': 'packaging',
    }


class ReportStates(StatesGroup):
    """
        Состояния для отправки отчёта
    """
    select_type = State()
    select_category = State()
    select_product = State()
    select_role = State()
    select_count = State()
    select_marriage = State()
    select_comment = State()

    # сщстояния для почасового отчёота
    select_category_2 = State()
    select_count_2 = State()
    select_comment_2 = State()


# обработка отчёта о работе по окладу внизу
async def start_report(
        message: types.Message,
        state: FSMContext,
        ):
    await state.set_state(ReportStates.select_type)
    await message.answer(
        'Выберите категорию',
        reply_markup=SELECT_TYPE_REPORT
        )


# хендлеры почасовой оплаты
async def select_type_1(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await state.set_state(ReportStates.select_category)
    cat_list = await get_сategory_list(session_maker)
    await message.answer(
        'Выберите категорию',
        reply_markup=generate_categorys_board(cat_list)
        )


async def select_category(
        query: types.CallbackQuery,
        callback_data: CategoryCD,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await state.update_data(select_category=callback_data.category_name)
    await state.set_state(ReportStates.select_product)
    products_list = await get_products_list(
        session_maker,
        callback_data.category_name
        )
    await SendMessage(
        text='Выберите наименование детали',
        chat_id=query.from_user.id,
        reply_markup=generate_product_board(products_list)
        )


async def select_product(
        query: types.CallbackQuery,
        callback_data: ProductCD,
        state: FSMContext,
        session_maker: sessionmaker
        ):
    await state.update_data(select_product=callback_data.name)
    await state.set_state(ReportStates.select_role)
    user_roles = await get_user_roles(
        int(query.from_user.id),
        session_maker)
    await SendMessage(
        text='Укажите роль в которой вы выполниля работу',
        chat_id=query.from_user.id,
        reply_markup=generate_roles_board(user_roles)
        )


async def select_role(
        query: types.CallbackQuery,
        callback_data: UserRoleCD,
        state: FSMContext,
        ):
    await state.update_data(select_role=callback_data.name)
    await state.set_state(ReportStates.select_count)
    await SendMessage(
        text='Укажите количество обработанной продукции (Цифрой)',
        chat_id=query.from_user.id,
        )


async def select_count(
        message: types.Message,
        state: FSMContext,
        ):
    await state.update_data(select_count=message.text)
    await state.set_state(ReportStates.select_marriage)
    await SendMessage(
        text='Укажите количество брака (Цифрой)',
        chat_id=message.from_user.id,
        )


async def select_marriage(
        message: types.Message,
        state: FSMContext,
        ):
    await state.update_data(select_marriage=message.text)
    await state.set_state(ReportStates.select_comment)
    await SendMessage(
        text='Оставьте комментарий',
        chat_id=message.from_user.id,
        )


async def send_report(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):

    report_data = {}
    data = await state.get_data()
    await state.clear()
    user: User = await get_user(message.from_user.id, session_maker)
    product: Product = await get_product(
        session_maker, data['select_category'], data['select_product'])

    report_data['username'] = user.name
    report_data['product'] = product.name
    report_data['user_id'] = user.user_id
    report_data['deta'] = datetime.today().strftime('%Y-%m-%d')
    report_data['count'] = float(data.get('select_count'))
    report_data['prise'] = (
        float(product.__getattribute__(ROLE_NAMES[data['select_role']]))
        )
    report_data['salary'] = 0
    report_data['comment'] = message.text
    report_data['amount'] = report_data.get('prise') * report_data.get('count')
    report_data['marriage'] = float(data.get('select_marriage'))

    await create_report(report_data, session_maker)
    await add_reports(report_data, message.from_user.id)
    await SendMessage(
        text=f'Отчёт о работе на сумму {report_data.get("amount")} отправлен',
        chat_id=message.from_user.id,
        reply_markup=START_WORKER_BOARD
        )


# -------------- Обработка почасовой оплаты -------------- #
async def select_type_2(
        message: types.Message,
        state: FSMContext,
        ):
    await state.set_state(ReportStates.select_category_2)
    salarys = await read_salarys()
    await message.answer(
        'Укажите размер ставки',
        reply_markup=simple_generate_board(salarys)
        )


async def select_category_2(
        query: types.CallbackQuery,
        callback_data: SalarysCD,
        state: FSMContext,
        ):
    await state.update_data(select_category_2=callback_data.salary)
    await state.set_state(ReportStates.select_count_2)
    await SendMessage(
        text='Укажите количество отработанных часов (Цифрой)',
        chat_id=query.from_user.id,
        )


async def select_count_2(
        message: types.Message,
        state: FSMContext,
        ):
    await state.update_data(select_count_2=message.text)
    await state.set_state(ReportStates.select_comment_2)
    await SendMessage(
        text='Оставьте комментарий',
        chat_id=message.from_user.id,
        )


async def send_report_2(
        message: types.Message,
        state: FSMContext,
        session_maker: sessionmaker
        ):

    report_dt = {}
    data = await state.get_data()
    await state.clear()
    user: User = await get_user(message.from_user.id, session_maker)

    report_dt['username'] = user.name
    report_dt['product'] = '-'
    report_dt['user_id'] = user.user_id
    report_dt['deta'] = datetime.today().strftime('%Y-%m-%d')
    report_dt['count'] = float(data.get('select_count_2'))
    report_dt['prise'] = 0
    report_dt['salary'] = float(data['select_category_2'])
    report_dt['comment'] = message.text
    report_dt['amount'] = report_dt.get('salary') * report_dt.get('count')
    report_dt['marriage'] = 0

    await create_report(report_dt, session_maker)
    await add_reports(report_dt, message.from_user.id)
    await SendMessage(
        text=f'Отчёт о работе на сумму {report_dt.get("amount")} отправлен',
        chat_id=message.from_user.id,
        reply_markup=START_WORKER_BOARD
        )
