from telegram import ReplyKeyboardMarkup


def main_menu_keyboard():
    return ReplyKeyboardMarkup([
        ['Меню Binance', 'Меню акций']
    ], row_width=1, resize_keyboard=True)


def main_binance_keyboard():
    return ReplyKeyboardMarkup([
        ['Создать ордер', 'Отменить ордер'],
        ['Открытые ордеры', 'Узнать баланс'],
        ['Текущий курс', 'История торгов'],
        ['Начать отслеживать'],
        ['Главное меню', 'Помощь']
    ], row_width=1, resize_keyboard=True)


def main_shares_keyboard():
    return ReplyKeyboardMarkup([
        ['Мои инструменты'],
        ['Добавить', 'Изменить/Удалить'],
        ['Главное меню', 'Помощь']
    ], row_width=1, resize_keyboard=True)


def cancel_keyboard():
    return ReplyKeyboardMarkup([
        ['Отмена']
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


def edit_choose_keyboard():
    return ReplyKeyboardMarkup([
        ['Максимальная', 'Минимальная'],
        ['Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def another_pair_keyboard():
    return ReplyKeyboardMarkup([
        ['Другая пара', 'Отмена']
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)
