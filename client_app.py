from settings import *
from binance_utils import BinanceClient
from pprint import PrettyPrinter


pp = PrettyPrinter()


def main():

    binance_client = BinanceClient()
    binance_client.set_order('BTC', 'USDT')
    print(binance_client.get_average_price('ETC', 'USDT'))
    print(binance_client.get_average_price('BTC', 'USDT'))
    print(binance_client.get_all_open_orders())
    print(binance_client.get_balance())

    # pp.pprint(close_order('BTC','USDT',SOME_ORDER_ID)) # Проверить можно только с реальным ордером.


if __name__ == "__main__":
    main()
