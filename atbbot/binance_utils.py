import logging
from datetime import datetime
from functools import wraps

from settings import BINANCE_API_KEY
from settings import SECRET_KEY
from settings import EXCEPTIONS

from binance.client import Client
from binance.enums import (SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT,
                           ORDER_TYPE_MARKET, TIME_IN_FORCE_GTC)

logging.basicConfig(filename='binance.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)


def wrap_try_except(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except EXCEPTIONS as ex:
            logging.info(f'Возникла ошибка - {ex}')
    return wrapper


class BinanceClient():

    def __init__(self):
        self.client = Client(BINANCE_API_KEY, SECRET_KEY)

    @wrap_try_except
    def __make_client_call(self, method_name, *args, **kwargs):
        result = getattr(self.client, method_name)(*args, **kwargs)
        return result

    def set_order(self, ticker_1, ticker_2, order_type, side, quantity, price=None):
        """"
        Выставляет ордер с заданными параметрами.
        Собираем из аргументов запрос на возможные оредра:
        Лимитный ордер на покупку,
        Лимитный ордер на продажу,
        Маркет ордер на покупку,
        Маркет ордер на продажу.
        """
        formated_call = 'order_'
        if order_type == 'limit':
            order_type = ORDER_TYPE_LIMIT
            formated_call += 'limit'
        elif order_type == 'market':
            order_type = ORDER_TYPE_MARKET
            formated_call += 'market'
        elif side == 'buy':
            side = SIDE_BUY
            formated_call += 'buy'
        elif side == 'sell':
            side = SIDE_SELL
            formated_call += 'sell'

        order = self.__make_client_call(f'{formated_call}',
                                        symbol=f'{ticker_1}{ticker_2}',
                                        side=f'{side}',
                                        type=type,
                                        timeInForce=TIME_IN_FORCE_GTC,
                                        quantity=quantity,
                                        price=price
                                        )
        if order is not None:
            logging.info('Выполнено. ', order)
            return order

    def set_order_market_sell(self, ticker_1, ticker_2, quantity):

        order = self.__make_client_call('order_market_sell',
                                        symbol=f'{ticker_1}{ticker_2}',
                                        quantity=quantity,
                                        )
        if order is not None:
            logging.info('Выполнено. ', order)
            return order

    def set_order_market_buy(self, ticker_1, ticker_2, quantity):

        order = self.__make_client_call('order_market_buy',
                                        symbol=f'{ticker_1}{ticker_2}',
                                        quantity=quantity,
                                        )
        if order is not None:
            logging.info('Выполнено. ', order)
            return order

    def get_average_price(self, ticker_1, ticker_2):
        """ Возвращает текущую цену заданной пары. """

        avg_price = self.__make_client_call('get_avg_price', symbol=f'{ticker_1}{ticker_2}')

        if avg_price is not None:
            formated_avg_price = avg_price['price'] + " " + ticker_2
            logging.info(formated_avg_price)
            return formated_avg_price

    def get_all_open_orders(self):
        """ Возвращает список открытых сделок. """

        open_orders = self.__make_client_call('get_open_orders')
        if open_orders is not None:
            logging.info(f'Список открытых ордеров - {open_orders}')
            return open_orders

    def close_order(self, ticker_pair, orderId):
        """Метод закрывающий ордер."""

        # Проверяем есть ли ордер на закрытие.
        open_orders = self.__make_client_call('get_open_orders')
        for order in open_orders:
            if order.get('symbol') == f'{ticker_pair}' and order.get('orderId') == orderId:
                result = self.__make_client_call('cancel_order', symbol=f'{ticker_pair}', orderId=orderId)
                if result is not None:
                    logging.info('Выполнено.')
                    return result
                else:
                    logging.info('Ошибка.')
                logging.info('К сожалению, нет ордеров на закрытие.')

    def get_balance(self, full=True):
        """
        Возвращает баланс пользователя.
        Ecли вызванно с 'full=True',
        возвращаем полный баланс с замороженными средствами,
        которые могут находиться в ордерах.
         """

        # Получаем полную сводку по пользователю, включая весь баланс.
        info = self.__make_client_call('get_account')

        if info is not None:
            #  full - {'BTC': {'free': 2, 'locked': 12}, 'ETC': {...}
            #  not_full - {'BTC': 2, 'ETC': 12}
            balance = {}
            if full:
                for crypto in info['balances']:
                    if crypto['free'] != '0.00000000' and crypto['free'] != '0.00':
                        balance[crypto['asset']] = {'free': crypto['free']}

                    if crypto['locked'] != '0.00000000' and crypto['locked'] != '0.00':
                        try:
                            balance[crypto['asset']].update({'locked': crypto['locked']})
                        except KeyError:
                            balance[crypto['asset']] = {'locked': crypto['locked']}
                logging.info(balance)
                return balance
            else:
                for crypto in info['balances']:
                    if crypto['free'] != '0.00000000' and crypto['free'] != '0.00':
                        balance[crypto['asset']] = crypto['free']
                return balance

    def average_price(self, ticker_1, ticker_2):
        """ Возвращает значение цены заданой пары """

        price = self.__make_client_call('get_avg_price', symbol=f'{ticker_1}{ticker_2}')  # Получаем среднее значение цены за 5 мин.
        if price is not None:
            return round(float(price['price']), 1)

    def get_trade_history(self, ticker_1, ticker_2, is_time_stamp=True):
        """
        Возвращает историю торгов по заданой паре.
        По умолчанию возвращает c 'time' в time_stamp
        """

        trades = self.__make_client_call('get_my_trades', symbol=f'{ticker_1}{ticker_2}')
        if trades is not None and trades is not []:
            combined_trades = []
            for trade in trades:

                symbol = trade['symbol']
                quantity = trade['qty']
                quoteQty = trade['quoteQty']
                order_id = trade['orderId']
                price = trade['price']

                order = self.__make_client_call('get_order',
                                                symbol=f'{ticker_1}{ticker_2}',
                                                orderId=order_id)
                order_side = order['side']
                order_status = order['status']
                order_type = order['type']

                if is_time_stamp:
                    time = order['time']
                else:
                    # Деление на 1000 меняет формат с миллисекунд на секунды.
                    # Преобразуем datetime в строку.
                    time = datetime.fromtimestamp(order['time'] / 1000)
                    time = time.strftime("%d-%m-%Y, %H:%M:%S")
                logging.info(f'{symbol} {order_type} {order_side} {quantity} {quoteQty} {price} {order_status}')

                combined_trades.append(
                    {
                        'symbol': symbol, 'order_side': order_side,
                        'order_type': order_type, 'quantity': quantity,
                        'quoteQty': quoteQty, 'price': price,
                        'time': time
                    }
                    )
            logging.info(combined_trades)
            return combined_trades
        return None

    def get_symbol_info(self, symbol):
        """Получаем список параметров для торговли у запрашиваемого символа."""

        symbol_info = self.__make_client_call('get_symbol_info', symbol=symbol)
        return symbol_info


# Создаём экземпляр нашего класса.
binance_client = BinanceClient()
