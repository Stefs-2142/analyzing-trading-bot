from yahoo_fin import stock_info
import numpy


def get_ticker_price(ticker):
    """
    ������� ��������� ����� � ���������� ��� ������� ����
    ���� ������������� ������ ������ ������� - �������
    ���������� False
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
    ������� ��������� �� ���� ������ �� ���������� �������� ������ ����:
    [['YNDX', 45.5, 40.1],['AAPL', 350.1, 340.1]]
    ����� ���� ����������� ���������� ������, ���� ������/����������� ����
    ���������� - ��� ���������� �� True � ������������ � ����� ������.
    � ����� ����� ������� ���������� ������ ������� � ��������, ��� ����
    ���������� ����� �� ��� (���� �� ���� �� ���� ���������� - ������������
    ������ ������)
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
