from models import Asset
from keyboards import main_shares_keyboard, cancel_keyboard, skip_keyboard
from ticker_utils import get_ticker_price
from telegram.ext import ConversationHandler


import datetime
import logging


def add_start(update, context):
    update.message.reply_text(
        'Введите название тикера', reply_markup=cancel_keyboard()
    )
    context.user_data['ticker'] = [update.effective_user.id]
    return add_step_1


def add_step_1(update, context):
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
    print(context.user_data['ticker'])
    result = Asset().add_asset(context.user_data['ticker'])
    if result:
        update.message.reply_text(
            'Инструмент успешно добавлен!', reply_markup=main_shares_keyboard()
        )
        logging.info(f'Added asset {context.user_data["ticker"]}')
    else:
        update.message.reply_text(
            'Данный инструмент вами уже отслеживается.'
            'Если вы хотите удалить или внести изменения в '
            'параметры инструмента - воспользуйтесь '
            'соответствующими опциями.', reply_markup=main_shares_keyboard()
        )
    context.user_data.pop('ticker', None)
    return ConversationHandler.END
