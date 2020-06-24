from base import Base
from sqlalchemy import create_engine, Column
from sqlalchemy import BigInteger, Boolean, Integer, Text, Date, Float
from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key = True)
    user_id = Column('user_id', BigInteger)
    shares_user = Column('shares_user', Boolean)
    crypto_user = Column('crypto_user', Boolean)
    analytics_subscription = Column('analytics_subscription', Boolean)
    post_frequency = Column('post_frequency', Integer)
    analytics_frequency = Column('analytics_frequency', Integer)
    api_key = Column('api_key', Text)
        
    def __init__(self, user_id, shares_user, crypto_user,
                analytics_subscription, post_frequency, 
                analytics_frequency, api_key):
                
        self.user_id = user_id
        self.shares_user = shares_user
        self.crypto_user = crypto_user
        self.analytics_subscription = analytics_subscription
        self.post_frequency = post_frequency
        self.analytics_frequency = analytics_frequency
        self.api_key = api_key


class Asset(Base):
    __tablename__ = 'asset'
    
    id = Column(Integer, primary_key = True)
    user_id = Column('user_id', BigInteger)
    ticker = Column('ticker', Text)
    is_crypto = Column('is_crypto', Boolean)
    add_date = Column('add_date', Date)
    initial_price = Column('initial_price', Float)
    target_price = Column('target_price', Float)
    min_price = Column('min_price', Float)
        
    def __init__(self, user_id, ticker, is_crypto,
                add_date, initial_price, 
                target_price, min_price):
                
        self.user_id = user_id
        self.ticker = ticker
        self.is_crypto = is_crypto
        self.add_date = add_date
        self.initial_price = initial_price
        self.target_price = target_price
        self.min_price = min_price