import numpy
from binance_utils import binance_client as bc
from yahoo_fin import stock_info as si


def get_ticker_price(ticker):
    """
    Функция принимает тикер и возвращает его текущую цену
    Если идентификатор тикера указан неверно - функция
    возвращает False
    """
    try:
        price = si.get_live_price(ticker)
    except (AssertionError, KeyError):
        return False
    if numpy.isnan(price):
        return False
    else:
        return float(round(price, 8))


def get_prev_close(ticker):
    # Функция возвращает цену последнего закрытия для переданного тикера
    prev_close_price = si.get_quote_table(ticker).get('Previous Close')
    return prev_close_price


def ticker_pricing(tickers):
    """
    Функция принимает на вход список со вложенными списками такого вида:
    [[user_id, 'YNDX', 45.5, 40.1],[user_id, 'AAPL', 350.1, 340.1]]
    Через цикл прогоняется полученный список, если таргет/минимальная цены
    достигнуты - они заменяются на True и записываются в новый список.
    В конце цикла функция возвращает список списком в тикерами, где была
    достигнута любая из цен (если ни одна не была достигнута - возвращается
    пустой список)
    """
    alerted_tickers = []
    for ticker in tickers:
        user_id, ticker_id, t_price, m_price = ticker
        current_price = si.get_live_price(ticker_id)
        if t_price != 0:
            if current_price >= t_price:
                alerted_tickers.append([user_id, ticker_id, True, m_price])
        if m_price != 0:
            if current_price <= m_price:
                alerted_tickers.append([user_id, ticker_id, t_price, True])
    return alerted_tickers


def ticker_crypto_pricing(tickers):
    """
    Функция принимает на вход список со вложенными списками такого вида:
    [[user_id, 'BTC/USDT', 11200.25, 13000.1],[user_id, 'ETC/USDT', 350.1, 340.1]]
    Через цикл прогоняется полученный список, если таргет/минимальная цены
    достигнуты - они заменяются на True и записываются в новый список.
    В конце цикла функция возвращает список списком в тикерами, где была
    достигнута любая из цен (если ни одна не была достигнута - возвращается
    пустой список)
    """
    alerted_tickers = []
    for ticker in tickers:
        user_id, ticker_id, t_price, m_price = ticker
        current_price = bc.get_average_price(ticker_id.split('/')[0], ticker_id.split('/')[1])
        current_price = float(current_price.split(' ')[0])
        if t_price != 0:
            if current_price >= t_price:
                alerted_tickers.append([user_id, ticker_id, True, m_price])
        if m_price != 0:
            if current_price <= m_price:
                alerted_tickers.append([user_id, ticker_id, t_price, True])
    return alerted_tickers
