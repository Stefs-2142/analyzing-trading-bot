from yahoo_fin import stock_info
import numpy


def get_ticker_price(ticker):
    """
    Функция принимает тикер и возвращает его текущую цену
    Если идентификатор тикера указан неверно - функция
    возвращает False
    """
    try:
        price = stock_info.get_live_price(ticker)
    except (AssertionError, KeyError):
        return False
    if numpy.isnan(price):
        return False
    else:
        return float(round(price, 8))


def ticker_pricing(tickers):
    """
    Функция принимает на вход список со вложенными списками такого вида:
    [['YNDX', 45.5, 40.1],['AAPL', 350.1, 340.1]]
    Через цикл прогоняется полученный список, если таргет/минимальная цены
    достигнуты - они заменяются на True и записываются в новый список.
    В конце цикла функция возвращает список списком в тикерами, где была
    достигнута любая из цен (если ни одна не была достигнута - возвращается
    пустой список)
    """
    alerted_tickers = []
    for ticker in tickers:
        ticker_name = ticker[0]
        target_price = ticker[1]
        min_price = ticker[2]
        current_price = stock_info.get_live_price(ticker_name)
        if current_price >= target_price:
            alerted_tickers.append([ticker_name, True, min_price])
        elif current_price <= min_price:
            alerted_tickers.append([ticker_name, target_price, True])
    return alerted_tickers
