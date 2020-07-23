from models import Asset
from keyboards import main_shares_keyboard
from ticker_utils import get_ticker_price, get_prev_close


def asset_view(update, context):
    """
    Выгружаем все отслеживаемые пользователем инструменты из БД
    """
    user_assets = Asset().get_user_assets(update.effective_user.id)
    if user_assets:
        update.message.reply_text('Сейчас отслеживаются следующие инструменты:')
        """
        Циклом проходим по каждому инструменту:
        Получаем текущую стоимость актива и стоимость последнего закрытия
        Добавляем эти две стоимости в список, который получили из БД и
        передаем его в соседнюю функцию для компиляции сообщений пользователю
        """
        for asset in user_assets:
            ticker = asset[0]
            asset.append(get_ticker_price(ticker))
            asset.append(get_prev_close(ticker))
            reply_text = compile_message(asset)
            update.message.reply_text(reply_text)
    else:
        update.message.reply_text('Ещё нет отсеживаемых инструментов.')


def compile_message(asset):
    (
        ticker, add_date, initial_price, target_price, min_price,
        current_price, prev_close_price
    ) = asset
    reply = f'Идентификатор инструмента:\r\n{ticker}\r\n\r\n'
    reply += f'Начальная цена:\r\n{initial_price}\r\n\r\n'
    reply += f'Текущая цена:\r\n{current_price}\r\n\r\n'
    if target_price != 0:
        reply += f'Целевая стоимость:\r\n{target_price}\r\n\r\n'
    if min_price != 0:
        reply += f'Минимальная стоимость:\r\n{min_price}\r\n\r\n'
    """
    Считаем процент изменение цены с начала отслеживания (т.е. от
    цены, которая была на момент когда пользователь добавил себе
    этот инструмент)
    """
    overall_change = round(
        ((initial_price - current_price) * 100 / initial_price) * -1, 3
    )
    reply += f'Изменение цены за всё время:\r\n{overall_change}%\r\n\r\n'
    """
    Считаем процент изменения цены за сегодня, т.е. от цены последнего закрытия
    """
    day_change = round(
        ((prev_close_price - current_price) * 100 / prev_close_price) * -1, 3
    )
    reply += f'Изменение цены за сегодня:\r\n{day_change}%\r\n\r\n'
    return reply
