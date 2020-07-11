from binance.client import Client
from binance.enums import SIDE_BUY, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from settings import API_KEY, SECRET_KEY, EXCEPTION_LIST
import logging
from tasks import alert_status


client = Client(API_KEY, SECRET_KEY)
logging.basicConfig(filename='binance.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)


class BinanceClient():

    def __init__(self):
        self.client = Client(API_KEY, SECRET_KEY)

    def set_order(self, ticket_1, ticket_2):
        """" Выставляет ордер с заданными параметрами. """

        try:
            order = client.create_test_order(  # Создаём тестовый ордер в тестовой сети.
                symbol=f'{ticket_1}{ticket_2}',
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=1,
                price=9800)
        except EXCEPTION_LIST as ex:
            logging.info(f'Возникла ошибка - {ex}')
        else:
            logging.info('Выполнено.')
            return order

    def get_average_price(self, ticket_1, ticket_2):
        """ Возвращает текущую цену заданной пары. """

        try:
            avg_price = client.get_avg_price(symbol=f'{ticket_1}{ticket_2}')  # Получаем среднее значение цены за 5 мин.
        except EXCEPTION_LIST as ex:
            logging.info(f'Возникла ошибка - {ex}')
        else:
            formated_avg_price = str(round(float(avg_price['price']), 1)) + " " + str(ticket_2)
            logging.info(formated_avg_price)
            return formated_avg_price

    def get_all_open_orders(self):
        """ Возвращает список открытых сделок. """

        try:
            orders = client.get_open_orders()  # Получаем список открытых сделок.
        except EXCEPTION_LIST as ex:
            logging.info(f'Возникла ошибка - {ex}')
        else:
            logging.info(f'Список открытых ордеров - {orders}')
            return orders

    def close_order(self, ticket_1, ticket_2, orderId):
        """ Закрывает ордер. """

        orders = self.get_all_open_orders()  # Проверяем есть ли ордер на закрытие.
        for order in orders:
            if order.get('symbol') == f'{ticket_1}{ticket_2}' and order.get('orderId') == orderId:
                try:
                    result = client.cancel_order(symbol=f'{ticket_1}{ticket_2}', orderId='orderId')
                    logging.info('Выполнено.')
                    return result
                except EXCEPTION_LIST as ex:
                    logging.info(f'Возникла ошибка - {ex}')
            else:
                return logging.info('К сожалению, нет ордеров на закрытие.')

    def get_balance(self):
        """ Возвращает баланс пользователя. """

        info = client.get_account()
        balance = {}  # Создаём словарь с балансом пользователя.{'BTC':2, 'ETC':12}
        for crypto in info['balances']:
            if crypto['free'] != '0.00000000':
                balance[crypto['asset']] = crypto['free']
        logging.info(balance)
        return balance

    def average_price(self, ticket_1, ticket_2):
        """ Возвращает значение цены заданой пары """
        try:
            price = client.get_avg_price(symbol=f'{ticket_1}{ticket_2}')  # Получаем среднее значение цены за 5 мин.
        except EXCEPTION_LIST as ex:
            logging.info(f'Возникла ошибка - {ex}')
        else:
            return round(float(price['price']), 1)

    def get_trade_history(self, ticket_1, ticket_2):
        """ Возвращает историю торгов по заданой паре. """

        try:
            trades = client.get_my_trades(symbol=f'{ticket_1}{ticket_2}')
            combined_trades = []
            for trade in trades:

                symbol = trade['symbol']
                quantity = trade['qty']
                quoteQty = trade['quoteQty']
                order_id = trade['orderId']

                order = client.get_order(
                    symbol=f'{ticket_1}{ticket_2}',
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

        except EXCEPTION_LIST as ex:
            logging.info(f'Возникла ошибка - {ex}')
        else:
            return combined_trades

    def set_alert(self, ticket_1, ticket_2, target):

        """ Устанавливает отслеживание вхождения цены в алертное состояние. """

        alert_status.delay(ticket_1, ticket_2, target)
        logging.info('Таргет установлен.')
        return True
