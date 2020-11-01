import os

from binance.exceptions import *

TELEGRAM_API_KEY = os.environ['TELEGRAM_API_KEY']
DB_CONNECT = os.environ['DATABASE_URL']
BACKEND_PATH = os.environ['REDIS_URL']
BROKER_PATH = os.environ['REDIS_URL']
SENTRY_URL = os.environ['SENTRY_DSN']
BINANCE_API_KEY = os.environ['BINANCE_API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
ADMIN_ID = 364447727

EXCEPTIONS = (
                BinanceRequestException, BinanceAPIException, BinanceOrderException,
                BinanceOrderMinAmountException, BinanceOrderMinPriceException,
                BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
                BinanceOrderInactiveSymbolException
                )
