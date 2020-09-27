from telegram.ext import ConversationHandler
from binance_utils import binance_client
from keyboards import cancel_keyboard, yes_no_keyboard, main_menu_keyboard
from handlers_utils import clear_all_crypto


def set_target(update, context):
    """Запрашиваем пару для установки цели."""

    update.message.reply_text(
        'Чтобы установить Alert пришлите пару в формате BTC USDT',
        reply_markup=cancel_keyboard()
        )
    return "set_target_step_1"


def choosing_pair_for_target(update, context):  # set_target_step_1
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
        return "set_target_step_1"

    # Сохраняем введёную пару тикеров.
    context.user_data['ticker_pair'] = ticker_pair

    # Делаем запрос к API и узнаём текущий курс.
    result = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    if result is not None:
        update.message.reply_text(
            f'Текущая цена заданной пары {result}\n'
            'Пожалуйста, введите цену на которой вы хотите получить уведомление.',
            reply_markup=cancel_keyboard()
        )
        return "set_target_step_2"

    # Возвращаем на шаг назад если пара тикеров невалидна.
    update.message.reply_text(
        'К сожалению, введена неверная пара, попробуйте ещё раз.',
        reply_markup=cancel_keyboard()
        )
    return "set_target_step_1"


def checking_price_for_target(update, context):  # set_target_step_2
    """Проверяем валидность введёной цены"""

    try:
        1 / float(update.message.text) and float(update.message.text)
    except (ValueError, TypeError, ZeroDivisionError) as err:
        update.message.reply_text(
            f'Введите цену ещё раз в формате "356.7", отличную от нуля.{err}',
            reply_markup=cancel_keyboard()
        )
        return "set_target_step_2"
    else:
        # Сохраняем цену для тарегта.
        target_price = update.message.text
        context.user_data['target_price'] = target_price
        # Забираем ранее сохранённую пару.
        ticker_pair = context.user_data['ticker_pair']
        # Формируем сообщение.
        message = f'Установить таргет для пары {ticker_pair} {target_price} {ticker_pair[1]}?'
        update.message.reply_text(message, reply_markup=yes_no_keyboard())
        return "set_target_step_3"


def aplying_target(update, context):  # set_target_step_3
    """Подтверждаем тартет и выставляем его."""

    if update.message.text != 'Да':
        update.message.reply_text(
            'Хорошо.',
            reply_markup=main_menu_keyboard()
            )
        clear_all_crypto(update, context)
        return ConversationHandler.END
    else:
        # Забираем ранее сохранённую пару и таргет.
        ticker_pair = context.user_data['ticker_pair']
        target_price = context.user_data['target_price']
        update.message.reply_text(
            f'Вы получите уведомление когда пара {ticker_pair} дотстигнет {target_price} {ticker_pair[1]}',
            reply_markup=main_menu_keyboard()
            )
        # TODO: Передаём в Celery задачу.

        clear_all_crypto(update, context)
        return ConversationHandler.END
