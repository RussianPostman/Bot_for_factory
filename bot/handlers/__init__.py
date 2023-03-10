from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from bot.handlers.keyboards.admin_kb import UserCD
from bot.handlers.keyboards.worker_kb import CategoryCD, ProductCD,\
    UserRoleCD, SalarysCD
from bot.handlers.commands import start, help, censel_hendler
from bot.handlers.admin.create_user import start_user_create, \
    UserStates, waiting_for_id, waiting_for_name, user_create
from bot.handlers.admin.delete_user import start_user_delete, user_delete, \
    DeleteUserStates
from bot.handlers.admin.synchronization import start_synchronization, \
    SynchronizationStates, synchronization_roles, synchronization_products
from bot.handlers.admin.is_admin_filter import IsAdminFilter
from bot.handlers.worker.send_report import start_report, select_product, \
    ReportStates, select_category, select_role, select_count, \
    select_marriage, send_report, select_type_1, select_type_2, \
    select_category_2, select_count_2, send_report_2
from bot.handlers.worker.money_info import money_info_today, money_info_month
from bot.handlers.admin.user_info import UserInfoStates, start_user_info, \
    user_info_month
from bot.handlers.admin.google_links import tables_list


__all__ = ['register_user_commands']


def register_user_commands(router: Router) -> Router:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())
    router.message.register(help, Command(commands=['help']))

    # хендлеры выхода из машины состояний
    router.message.register(censel_hendler, Command('cancel'), any_state)
    router.message.register(censel_hendler, F.text.casefold() == 'отмена' or 'Отмена', any_state)
    router.callback_query.register(censel_hendler, F.data == 'cancel', any_state)

    # отправка очёта
    router.message.register(start_report, F.text == 'Отправить отчёт о работе')
    # отчёт по сдельной работе
    router.message.register(
        select_type_1, ReportStates.select_type, F.text == 'Сдельная')
    router.callback_query.register(
        select_category, ReportStates.select_category, CategoryCD.filter(F.flag == '1'))
    router.callback_query.register(
        select_product, ReportStates.select_product, ProductCD.filter(F.flag == '1'))
    router.callback_query.register(
        select_role, ReportStates.select_role, UserRoleCD.filter(F.flag == '1'))
    router.message.register(select_count, ReportStates.select_count)
    router.message.register(select_marriage, ReportStates.select_marriage)
    router.message.register(send_report, ReportStates.select_comment)
    # отчёт по работае на окладе
    router.message.register(
        select_type_2, ReportStates.select_type, F.text == 'Почасовая')
    router.callback_query.register(
        select_category_2, ReportStates.select_category_2, SalarysCD.filter(F.flag == '1'))
    router.message.register(select_count_2, ReportStates.select_count_2)
    router.message.register(send_report_2, ReportStates.select_comment_2)

    # узнать сколько заработал сегодня
    router.message.register(money_info_today, F.text == 'Узнать cумму на сегоденя')
    router.message.register(money_info_month, F.text == 'Узнать сумму в этом месяце')

    # хендлеры админа:
    # создание пользователя
    router.message.register(start_user_create, F.text == 'Добавить пользователя')
    router.message.register(waiting_for_name, UserStates.waiting_for_name)
    router.message.register(waiting_for_id, UserStates.waiting_for_id)
    router.callback_query.register(user_create, UserStates.select_role, F.data == 'admin')
    router.callback_query.register(user_create, UserStates.select_role, F.data == 'worker')

    # удаление пользователя
    router.message.register(start_user_delete, IsAdminFilter('Удалить пользователя'))
    router.callback_query.register(
        user_delete, DeleteUserStates.waiting_for_id, UserCD.filter(F.flag == '1')
        )

    # информация о пользователе
    router.message.register(start_user_info, F.text == 'Информация о пользователе')
    router.callback_query.register(
        user_info_month, UserInfoStates.waiting_for_id, UserCD.filter(F.flag == '1')
        )

    # гугл ссылки
    router.message.register(tables_list, F.text == 'Перейти к Google таблицам')

    # хендлеры синхронизации бд
    router.message.register(start_synchronization, F.text == 'Синхронизация')
    router.callback_query.register(
        synchronization_roles, SynchronizationStates.chose, F.data == 'synchronization_roles'
        )
    router.callback_query.register(
        synchronization_products, SynchronizationStates.chose, F.data == 'synchronization_products')
