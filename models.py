from base import Session, Engine, Base
from sqlalchemy import create_engine, exists, Column, literal
from sqlalchemy import BigInteger, Boolean, Integer, Text, Date, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.exc


class User(Base):
    __tablename__ = 'users'

    session = Session()

    user_id = Column('user_id', BigInteger, primary_key=True)
    shares_user = Column('shares_user', Boolean)
    crypto_user = Column('crypto_user', Boolean)
    analytics_subscription = Column('analytics_subscription', Boolean)
    post_frequency = Column('post_frequency', Integer)
    analytics_frequency = Column('analytics_frequency', Integer)
    api_key = Column('api_key', Text)

    def add_user(self, user_data):

        (
            user_id_cand, shares_user_cand,
            crypto_user_cand, analytics_subscription_cand,
            post_frequency_cand, analytics_frequency_cand, api_key_cand,
        ) = user_data

        candidate_user = User(
                        user_id=user_id_cand,
                        shares_user=shares_user_cand,
                        crypto_user=crypto_user_cand,
                        analytics_subscription=analytics_subscription_cand,
                        post_frequency=post_frequency_cand,
                        analytics_frequency=analytics_frequency_cand,
                        api_key=api_key_cand
                        )
        self.session.add(candidate_user)

        try:
            self.session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            return False

    def del_user(self, del_user_id):
        candidate_user = self.session.query(User).get(del_user_id)

        try:
            self.session.delete(candidate_user)
            self.session.commit()
            return True
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            self.session.rollback()
            return False


class Asset(Base):
    __tablename__ = 'assets'

    session = Session()

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', BigInteger)
    ticker = Column('ticker', Text)
    is_crypto = Column('is_crypto', Boolean)
    add_date = Column('add_date', Date)
    initial_price = Column('initial_price', Float)
    target_price = Column('target_price', Float)
    min_price = Column('min_price', Float)

    def add_asset(self, asset_data):
        # ! Попробовать переписать в NamedTuple
        (
            user_id_cand, ticker_cand, is_crypto_cand, add_date_cand,
            initial_price_cand, target_price_cand, min_price_cand,
        ) = asset_data

        candidate_asset = Asset(
            user_id=user_id_cand,
            ticker=ticker_cand,
            is_crypto=is_crypto_cand,
            add_date=add_date_cand,
            initial_price=initial_price_cand,
            target_price=target_price_cand,
            min_price=min_price_cand,
            )
        if self.session.query(exists().where(Asset.user_id
                      == user_id_cand).where(Asset.ticker
                      == ticker_cand)).scalar():
            self.session.rollback()
            return False
        else:
            self.session.add(candidate_asset)
            self.session.commit()
            return True

    def del_asset(self, del_user_id, del_ticker):

        self.session.query(Asset).filter_by(user_id
                      =del_user_id).filter_by(ticker
                      =del_ticker).delete()

        self.session.commit()
