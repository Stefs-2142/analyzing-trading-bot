from settings import *
from binance_utils import *
from pprint import PrettyPrinter


pp = PrettyPrinter()


def main():

    set_order('BTC','USDT')
    print(get_average_price('ETC','USDT'))
    print(get_average_price('BTC','USDT'))
    print(get_all_open_orders())
    #pp.pprint(close_order('BTC','USDT',SOME_ORDER_ID)) # Проверить можно только с реальным ордером.
    
    
    


if __name__ == "__main__":
    main()
    