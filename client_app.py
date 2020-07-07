from binance_utils import BinanceClient
import logging


def main():

    logging.info("Клиент запущен.")
    binance_client = BinanceClient()
    binance_client.set_order('BTC', 'USDT')
    binance_client.get_average_price('ETC', 'USDT')
    binance_client.get_average_price('BTC', 'USDT')
    binance_client.get_all_open_orders()
    binance_client.get_balance()
    binance_client.get_trade_history('BTT', 'USDT')


if __name__ == "__main__":
    main()