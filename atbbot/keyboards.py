﻿from telegram import ReplyKeyboardMarkup

KEYBOARD_PERCENT_POOL = ['25%', '50%', '75%', '100%']
ORDERS_TYPE = ['Limit order', 'Market order']
ORDERS_SIDE = ['buy', 'sell']


def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        ['Меню Binance 🖥', 'Меню акций 📈']
    ], row_width=1, resize_keyboard=True)


def main_binance_keyboard():
    return ReplyKeyboardMarkup([
        ['Создать ордер ➕', 'Отменить ордер ➖'],
        ['Открытые ордеры 📝', 'Узнать баланс 💰'],
        ['Текущий курс 📊', 'История торгов 📖'],
        ['Уведомления 📮'],
        ['Главное меню 📂', 'Помощь 📎']
    ], row_width=1, resize_keyboard=True)


def main_shares_keyboard():
    return ReplyKeyboardMarkup([
        ['Мои инструменты 📈'],
        ['Добавить ➕', 'Изменить/Удалить ➖'],
        ['Главное меню 📂', 'Помощь 📎']
    ], row_width=1, resize_keyboard=True)


def main_crypto_shares_keyboard():
    return ReplyKeyboardMarkup([
        ['Отслеживаемые 👀'],
        ['Add ➕', 'Edit/Delete ➖'],
        ['Главное меню 📂', 'Помощь 📎']
    ], row_width=1, resize_keyboard=True)


def cancel_keyboard():
    return ReplyKeyboardMarkup([
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def back_keyboard():
    return ReplyKeyboardMarkup([
        ['Назад']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def skip_keyboard():
    return ReplyKeyboardMarkup([
        ['Пропустить'], ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def edit_del_keyboard():
    return ReplyKeyboardMarkup([
        ['Изменить', 'Удалить'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def edit_del_crypto_keyboard():
    return ReplyKeyboardMarkup([
        ['Edit', 'Delete'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def edit_choose_keyboard():
    return ReplyKeyboardMarkup([
        ['Максимальная', 'Минимальная'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def edit_choose_crypto_keyboard():
    return ReplyKeyboardMarkup([
        ['Max', 'Min'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def another_pair_keyboard():
    return ReplyKeyboardMarkup([
        ['Другая пара', 'Назад']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def another_pair_back_keyboard():
    return ReplyKeyboardMarkup([
        ['Другая пара', 'Назад']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def order_type_keyboard():
    return ReplyKeyboardMarkup([
        ORDERS_TYPE,
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def buy_sell_keyboard(balance_ticker_1, balance_ticker_2):
    return ReplyKeyboardMarkup([
        [f'Доступно {balance_ticker_1}', f'Доступно {balance_ticker_2}'],
        ORDERS_SIDE,
        ['Отмена'],
    ], one_time_keyboard=False, row_width=1, resize_keyboard=True)


def quantity_keyboard():
    return ReplyKeyboardMarkup([
        KEYBOARD_PERCENT_POOL,
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def aply_order_keyboard(order_side):
    return ReplyKeyboardMarkup([
        [f'{order_side}'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def numbers_keyboard(n):
    return ReplyKeyboardMarkup([
        (str(n) for n in range(1, n)),
        ['Назад']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def yes_no_keyboard():
    return ReplyKeyboardMarkup([
        ['Да', 'Нет'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)
