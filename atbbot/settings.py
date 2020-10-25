import os

from binance.exceptions import *

TELEGRAM_API_KEY = "1273602121:AAHyItK7iNe6sx7iMpSG6mgknM9Or7NTgxg"
DB_CONNECT = os.environ['DATABASE_URL']
BACKEND_PATH = "rpc://"
BROKER_PATH = "redis://localhost:6379/0"
BINANCE_API_KEY = 'cywfdaMkZBSUgWm3H1rDqg9jMzAUXIyiAQpybBvsoKIlSTuMYIqEGojKfUYZq9Kp'
SECRET_KEY = 'AGDZPw1pH6szTjmBExpRThMR9pnZ2rJ0K3oX8roEiHsEesAJvDfS7ScWLjESNcPJ'

EXCEPTION_LIST = (
                BinanceRequestException, BinanceAPIException, BinanceOrderException,
                BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                BinanceOrderInactiveSymbolException
                )

PROXY_URL = 'socks5://t2.learn.python.ru:1080'

USER_EMOJI = [':hourglass_flowing_sand:', ':arrow_backward:']
