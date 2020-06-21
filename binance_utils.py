from binance.client import Client
from binance.enums import *
from settings import API_KEY, SECRET_KEY, EXCEPTION_LIST
from pprint import PrettyPrinter



client = Client(API_KEY, SECRET_KEY)
pp = PrettyPrinter()


def set_order(ticket_1,ticket_2):
    """" Выставляет ордер с заданными параметрами. """
    
    try:
        order = client.create_test_order(
        symbol=f'{ticket_1}{ticket_2}',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=1,
        price=9800)
    except EXCEPTION_LIST as e:
        print (f"К сожалению, возникла ошибка {ex}. Попробуйте ещё раз.")
    else:
        print ("Выполнено.")
        return order # 


def get_historical_data():
    pass
    #historical_data(client.get_recent_trades(symbol='BTTBTC'))

    
def get_average_price(ticket_1,ticket_2):
    """ Возвращает текущую цену заданной пары. """

    try:
        avg_price = client.get_avg_price(symbol=f'{ticket_1}{ticket_2}')
    except EXCEPTION_LIST as ex:
        print (f"К сожалению, возникла ошибка {ex}. Попробуйте ещё раз.") 
    else:
        return avg_price['price'] + f' {ticket_2}'


def get_all_open_orders():
    """ Возвращает список открытых сделок. """

    try:
        orders = client.get_open_orders()
    except EXCEPTION_LIST as ex:
        print (f"К сожалению, возникла ошибка {ex}. Попробуйте ещё раз.") 
    else:
        return orders


def close_order(ticket_1,ticket_2,orderId):
    """ Закрывает ордер. """

    orders = get_all_open_orders()  #Проверяем если ли ордер на закрытие. 
    for order in orders:                      
        if order.get('sybmol') == ticket_1 and order.get('sybmol') == ticket_1 and ordet.get('orderId') == orderId:
            try:
                result = cancel_order(symbol=f'{ticket_1}{ticket_2}',orderId='orderId')
                print("Ордер успешно закрыт.")
                return result
            except EXCEPTION_LIST as ex:
                print (f"К сожалению, возникла ошибка {ex}. Попробуйте ещё раз.") 
        else:
            return 'К сожалению, нет ордеров на закрытие.'




    
    

