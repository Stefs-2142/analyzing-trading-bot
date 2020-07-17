from binance_utils import BinanceClient
import logging
from tasks import set_alert

binance_client = BinanceClient()


def main():

    logging.info("Клиент запущен.")
    set_alert.delay('ETC', 'USDT', 6)
    binance_client.set_order('BTC', 'USDT', 'limit', 'buy')
    binance_client.get_average_price('ETC', 'USDT')
    binance_client.get_average_price('BTC', 'USDT')
    binance_client.get_all_open_orders()
    binance_client.get_balance()
    binance_client.get_trade_history('BTT', 'USDT')


if __name__ == "__main__":
    main()
