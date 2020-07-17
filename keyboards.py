from telegram import ReplyKeyboardMarkup


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
