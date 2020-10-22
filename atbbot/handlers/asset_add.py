import datetime
import logging

from telegram.ext import ConversationHandler

from db.models import Asset

from keyboards import cancel_keyboard, main_shares_keyboard, skip_keyboard

from ticker_utils import get_ticker_price


def add_start(update, context):
    """
    Функции для добавления инструмента пользователем, в контекст по
    ходу функций записывают данные об инструменте, который в конце
    записывается в БД
    """
    update.message.reply_text(
        'Введите название тикера', reply_markup=cancel_keyboard()
    )
    # Сразу записываем в контекст id пользователя
    context.user_data['ticker'] = [update.effective_user.id]
    return add_step_1


def add_step_1(update, context):
    """
    Пытаемся получить цену введенного тикера.
    Если получаем True - всё ок. False - значит такого тикера
    не существует, зацикливаем повторный запрос тикера.
    """
    ticker = update.message.text.split()[0]
    ticker_current_price = get_ticker_price(ticker)
    if ticker_current_price is False:
        update.message.reply_text(
            'Введенный тикер не найден. Повторите ввод '
            'или нажмите кнопку "Отмена" чтобы прервать '
            'выполнение операции', reply_markup=cancel_keyboard()
        )
        return add_step_1
    current_date = f"{datetime.datetime.now():%Y-%m-%d}"
    """
    Записываем в контекст следующие переменные:
    - Название тикера
    - Характеристика, является ли тикер криптой или
      нет (!Всегда False, не реализовано)
    - Текущая дата
    - Текущая стоимость

    Далее запрашиваем у пользователя, хочет ли он указать
    иную начальную стоимость или использовать текущую
    """
    context.user_data['ticker'].extend([
        ticker, False, current_date, ticker_current_price
    ])
    update.message.reply_text(
        f'Текущая стоимость {ticker} - {ticker_current_price}. '
        'Если вы хотите отслеживать иную начальную стоимость - '
        'отправьте её ответным сообщением. Для продолжения нажмите'
        ' на кнопку "Пропустить"', reply_markup=skip_keyboard()
    )
    return add_step_2


def add_step_2(update, context):
    """
    Если пользователь решил указать иную начальную стоимость -
    выполняем две проверки:
    1) Является ли то что ввел пользователем float
    2) Не ввел ли пользователь значение <= нуля
    В обоих случаях производим повторный запрос стоимости у юзера

    Если всё ок - запрашиваем целевую стоимость
    """
    if update.message.text != 'Пропустить':
        error_text = (
            'Повторите ввод или нажмите кнопку '
            '"Пропустить" чтобы использовать текущую стоимость.'
        )
        try:
            ticker_current_price = float(update.message.text.replace(',', '.'))
        except ValueError:
            update.message.reply_text(
                f'В введенной стоимости присутствуют ошибки. {error_text}',
                reply_markup=skip_keyboard()
            )
            return add_step_2
        if ticker_current_price <= 0:
            update.message.reply_text(
                f'Стоимость не может быть равной или ниже нуля. {error_text}',
                reply_markup=skip_keyboard()
            )
            return add_step_2
        else:
            context.user_data['ticker'][4] = ticker_current_price
    update.message.reply_text(
        'Введите целевую стоимость актива (take-profit).'
        'Если вы не хотите отслеживать целевую стоимость - '
        'нажмите на кнопку "Пропустить"', reply_markup=skip_keyboard()
    )
    return add_step_3


def add_step_3(update, context):
    """
    Аналогичные проверки как в функции add_step_2
    Если всё ок - запрашиваем минимальную цену

    Дополнительно, если пользователь выбрал "Пропустить" -
    записываем такую цену как 0 (нужно будет для дальнейшего
    парсинга), аналогичная логика присутствует и в последней функции
    """
    if update.message.text == 'Пропустить':
        context.user_data['ticker'].append(0)
    else:
        error_text = (
            'Повторите ввод или нажмите кнопку "Пропустить".'
        )
        try:
            ticker_target_price = float(update.message.text.replace(',', '.'))
        except ValueError:
            update.message.reply_text(
                f'В введенной стоимости присутствуют ошибки. {error_text}',
                reply_markup=skip_keyboard()
            )
            return add_step_3
        if ticker_target_price <= 0:
            update.message.reply_text(
                f'Стоимость не может быть равной или ниже нуля. {error_text}',
                reply_markup=skip_keyboard()
            )
            return add_step_3
        else:
            context.user_data['ticker'].append(ticker_target_price)
    update.message.reply_text(
        'Введите минимальную стоимость актива (stop-loss).'
        'Если вы не хотите отслеживать целевую стоимость - '
        'нажмите на кнопку "Пропустить"', reply_markup=skip_keyboard()
    )
    return add_step_4


def add_step_4(update, context):
    """
    Аналогичные проверки как в функции add_step_2
    Если всё ок - записываем всё что накопилось в context в БД
    """
    if update.message.text == 'Пропустить':
        context.user_data['ticker'].append(0)
    else:
        error_text = (
            'Повторите ввод или нажмите кнопку "Пропустить".'
        )
        try:
            ticker_min_price = float(update.message.text.replace(',', '.'))
        except ValueError:
            update.message.reply_text(
                f'В введенной стоимости присутствуют ошибки. {error_text}',
                reply_markup=skip_keyboard()
            )
            return add_step_4
        if ticker_min_price <= 0:
            update.message.reply_text(
                f'Стоимость не может быть равной или ниже нуля. {error_text}',
                reply_markup=skip_keyboard()
            )
            return add_step_4
        else:
            context.user_data['ticker'].append(ticker_min_price)
    # Записываем содержимое context в БД и получаем результат
    result = Asset().add_asset(context.user_data['ticker'])
    # Если результат True - извещаем пользоваеля
    if result:
        update.message.reply_text(
            'Инструмент успешно добавлен!', reply_markup=main_shares_keyboard()
        )
        logging.info(f'Added asset {context.user_data["ticker"]}')
    else:
        """
        Если результат False, то это значит, что инструмент уже отслеживается,
        извещаем юзера
        """
        update.message.reply_text(
            'Данный инструмент вами уже отслеживается.'
            'Если вы хотите удалить или внести изменения в '
            'параметры инструмента - воспользуйтесь '
            'соответствующими опциями.', reply_markup=main_shares_keyboard()
        )
    context.user_data.pop('ticker', None)
    return ConversationHandler.END
