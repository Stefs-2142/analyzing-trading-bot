from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT
from binance.enums import ORDER_TYPE_MARKET, TIME_IN_FORCE_GTC
from settings import BINANCE_API_KEY, SECRET_KEY, EXCEPTION_LIST
import logging
from functools import wraps


client = Client(BINANCE_API_KEY, SECRET_KEY)
logging.basicConfig(filename='binance.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)


def wrap_try_except(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except EXCEPTION_LIST as ex:
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

    def get_average_price(self, ticker_1, ticker_2):
        """ Возвращает текущую цену заданной пары. """

        avg_price = self.__make_client_call('get_avg_price', symbol=f'{ticker_1}{ticker_2}')

        if avg_price is not None:
            formated_avg_price = str(round(float(avg_price['price']), 3)) + " " + str(ticker_2)
            logging.info(formated_avg_price)
            return formated_avg_price

    def get_all_open_orders(self):
        """ Возвращает список открытых сделок. """

        open_orders = self.__make_client_call('get_open_orders')  # Получаем список открытых сделок.
        if open_orders is not None:
            logging.info(f'Список открытых ордеров - {open_orders}')
            return open_orders

    def close_order(self, ticker_pair, orderId):
        """ Закрывает ордер. """

        open_orders = self.__make_client_call('get_open_orders')  # Проверяем есть ли ордер на закрытие.
        for order in open_orders:
            if order.get('symbol') == f'{ticker_pair}' and order.get('orderId') == orderId:
                result = self.__make_client_call('cancel_order', symbol=f'{ticker_pair}', orderId=orderId)
                if result is not None:
                    logging.info('Выполнено.')
                    return result
                else:
                    logging.info('Ошибка.')
                    return

                logging.info('К сожалению, нет ордеров на закрытие.')
                return

    def get_balance(self):
        """ Возвращает баланс пользователя. """

        # Получаем полную сводку по пользователю, включая весь баланс.
        info = self.__make_client_call('get_account')

        if info is not None:
            # Создаём словарь с балансом пользователя.
            # {'BTC': {'free': 2, 'locked': 12}, 'ETC': {...}
            balance = {}

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

    def average_price(self, ticker_1, ticker_2):
        """ Возвращает значение цены заданой пары """

        price = self.__make_client_call('get_avg_price', symbol=f'{ticker_1}{ticker_2}')  # Получаем среднее значение цены за 5 мин.
        if price is not None:
            return round(float(price['price']), 1)

    def get_trade_history(self, ticker_1, ticker_2):
        """ Возвращает историю торгов по заданой паре. """

        trades = self.__make_client_call('get_my_trades', symbol=f'{ticker_1}{ticker_2}')
        if trades is not None:
            combined_trades = []
            for trade in trades:

                symbol = trade['symbol']
                quantity = trade['qty']
                quoteQty = trade['quoteQty']
                order_id = trade['orderId']

                order = self.__make_client_call('get_order',
                                                symbol=f'{ticker_1}{ticker_2}',
                                                orderId=order_id)

                order_side = order['side']
                order_status = order['status']
                order_type = order['type']
                price = order['price']
                logging.info(f'{symbol} {order_type} {order_side} {quantity} {quoteQty} {price} {order_status}')

                combined_trades.append(
                    {'symbol': symbol, 'order_side': order_side,
                        'order_type': order_type, 'quantity': quantity,
                        'quoteQty': quoteQty, 'price': price})
            logging.info(combined_trades)
            return combined_trades


# Создаём экземпляр нашего класса.
binance_client = BinanceClient()
