from binance.client import Client
from binance.exceptions import *
from binance.enums import *
from settings import *



binance_client = Client(API_KEY, SECRET_KEY)


def set_order(ticket_1,ticket_2):
    """" Задаём пользовательские аргументы вызову метода. """

    
    try:
        order = binance_client.create_test_order(
        symbol=f'{ticket_1}{ticket_2}',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=1,
        price=9800)
    except (BinanceRequestException, BinanceAPIException, BinanceOrderException, 
            BinanceOrderMinAmountException, BinanceOrderMinPriceException,
            BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException) as e:
        print (f"К сожалению, возникла ошибка {e}. Попробуйте ещё раз.")
    else:
        print ("Выполнено.")
        
    

