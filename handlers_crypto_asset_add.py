from telegram.ext import ConversationHandler
from binance_utils import binance_client
from keyboards import cancel_keyboard, yes_no_keyboard, main_menu_keyboard
from handlers_utils import clear_all_crypto

from models import Asset
import datetime


def add_crypto(update, context):
    """Запрашиваем пару для установки уведомления."""

    update.message.reply_text(
        'Чтобы установить Alert пришлите пару в формате BTC USDT',
        reply_markup=cancel_keyboard()
        )
    # Сразу записываем в контекст id пользователя
    context.user_data['ticker'] = [update.effective_user.id]
    return "add_crypto_step_1"


def choosing_pair_for_target(update, context):  # add_crypto_step_1
    """
    Проверям валидность введёной пары тикеров для ордера
    """

    # Формируем пару тикеров из прошлого пользовательского ввода.
    ticker_pair = update.message.text.upper().split(' ')

    # Провереяем что пользователь ввёл 2 тикера.
    if len(ticker_pair) != 2:
        update.message.reply_text(
            'К сожалению, введена неверная пара, попробуйте ещё раз'
            ' или нажмите "Отмена" для завершения операции.',
            reply_markup=cancel_keyboard()
        )
        return "add_crypto_step_1"

    # Делаем запрос к API и узнаём текущий курс.
    current_price = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    if current_price is not None:
        update.message.reply_text(
            f'Текущая цена заданной пары {current_price}\n'
            'Пожалуйста, введите цену на которой вы хотите получить уведомление.',
            reply_markup=cancel_keyboard()
        )
        current_date = f"{datetime.datetime.now():%Y-%m-%d}"

        # Сохраняем введёную пару тикеров, текущую цену и дату добавления.
        context.user_data['ticker'].extend(
            [ticker_pair, True, current_date, current_price.split(' ')[0]])

        return "add_crypto_step_2"

    # Возвращаем на шаг назад если пара тикеров невалидна.
    update.message.reply_text(
        'К сожалению, введена неверная пара, попробуйте ещё раз.',
        reply_markup=cancel_keyboard()
        )
    return "add_crypto_step_1"


def checking_price_for_target(update, context):  # add_crypto_step_2
    """Проверяем валидность введёной цены"""

    try:
        1 / float(update.message.text) and float(update.message.text)
    except (ValueError, TypeError, ZeroDivisionError) as err:
        update.message.reply_text(
            f'Введите цену отличную от нуля.\nВы ввели {update.message.text}',
            reply_markup=cancel_keyboard()
        )
        return "add_crypto_step_2"
    else:
        # Сохраняем цену для тарегта.
        target_price = update.message.text
        context.user_data['ticker'].append(target_price)
        context.user_data['ticker'].append(0)
        # Забираем ранее сохранённую пару.
        ticker_pair = context.user_data['ticker'][1]

        # Формируем сообщение.
        message = f'Установить отслеживание для пары {ticker_pair[0]}/{ticker_pair[1]}'
        message += f' на цену {target_price} {ticker_pair[1]}?'
        update.message.reply_text(message, reply_markup=yes_no_keyboard())
        return "add_crypto_step_3"


def aplying_target(update, context):  # add_crypto_step_3
    """Подтверждаем тартет и выставляем его."""

    if update.message.text != 'Да':
        update.message.reply_text(
            'Хорошо.',
            reply_markup=main_menu_keyboard()
            )
        clear_all_crypto(update, context)
        return ConversationHandler.END
    else:
        context.user_data['ticker'][1] = context.user_data['ticker'][1][0] + f"/{context.user_data['ticker'][1][1]}"
        result = Asset().add_asset(context.user_data['ticker'])
        if result:
            # Забираем ранее сохранённую пару и таргет.
            ticker_pair = context.user_data['ticker'][1]
            target_price = context.user_data['ticker'][5]
            # Формируем сообщение.
            message = f'Вы получите уведомление, когда пара {ticker_pair}\n'
            message += f"дотстигнет цены - {target_price} {ticker_pair.split('/')[1]}"
            update.message.reply_text(message, reply_markup=main_menu_keyboard())

            # TODO: Передаём в Celery задачу.

            clear_all_crypto(update, context)
            return ConversationHandler.END
