import sqlalchemy.exc
from .base import session, Base
from sqlalchemy import (
    exists, Column,
    BigInteger, Boolean, Integer, Text, Date, Float
)


class User(Base):
    __tablename__ = 'users'

    user_id = Column('user_id', BigInteger, primary_key=True)
    shares_user = Column('shares_user', Boolean)
    crypto_user = Column('crypto_user', Boolean)
    analytics_subscription = Column('analytics_subscription', Boolean)
    post_frequency = Column('post_frequency', Integer)
    analytics_frequency = Column('analytics_frequency', Integer)
    api_key = Column('api_key', Text)

    def add_user(self, user_data):
        """
        Функция принимает на вход список с данными пользователя
        На основании списка функция создает объект пользователя
        После этого функция пытается добавить новый объект в БД
        Если происходит ошибка (пользователь с таким ID уже есть) -
        функция возвращает False, если все ок - True
        ! Попробовать переписать в NamedTuple
        """
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
        session.add(candidate_user)

        try:
            session.commit()
            return True
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            return False

    def del_user(self, del_user_id):
        """
        Функция удаляет пользователя из БД
        Единственное применение, если пользователь стопнул бота, но
        бот попытался отправить нотис пользователю, при таком сценарии -
        удаление юзера, есть обработчик ошибок,
        но я не уверен что он потребуется хоть когда-то
        """
        candidate_user = session.query(User).get(del_user_id)

        try:
            session.delete(candidate_user)
            session.commit()
            return True
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            session.rollback()
            return False

    def get_shares_users(self):
        """
        Функция отдает ID пользователей, которые следят за
        акциями в виде обычного списка
        """
        raw_users = session.query(
                User
            ).filter(
                User.shares_user
            ).all()

        users = [user.user_id for user in raw_users]

        return users

    def get_crypto_users(self):
        """
        Функция отдает ID пользователей, которые следят за
        криптой в виде обычного списка
        """
        raw_users = session.query(
                User
            ).filter(
                User.crypto_user
            ).all()

        users = [user.user_id for user in raw_users]

        return users

    def get_analytics_users(self):
        """
        Функция отдает ID пользователей, которые подписаны на аналитику
        """
        raw_users = session.query(
                User
            ).filter(
                User.analytics_subscription
            ).all()

        users = [user.user_id for user in raw_users]

        return users

    def get_api_key(self, query_user_id):
        """
        Функция отдает api ключ запрошенного пользователя строкой
        """
        user_key = session.query(
                User
            ).filter_by(
                user_id=query_user_id
            ).first().api_key

        return user_key


class Asset(Base):
    __tablename__ = 'assets'

    session = session

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', BigInteger)
    ticker = Column('ticker', Text)
    is_crypto = Column('is_crypto', Boolean)
    add_date = Column('add_date', Date)
    initial_price = Column('initial_price', Float)
    target_price = Column('target_price', Float)
    min_price = Column('min_price', Float)

    def add_asset(self, asset_data):
        """
        Функция принимает на вход список с данными по инструменту
        На основании списка функция создает объект инструмента
        После этого функция пытается добавить новый объект в БД
        Если происходит ошибка (если пара юзера и инструмента уже есть) -
        функция возвращает False, если все ок - True
        ! Попробовать переписать в NamedTuple
        """
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
        if session.query(
                exists().where(
                    Asset.user_id == user_id_cand
                ).where(
                    Asset.ticker == ticker_cand
                )).scalar():

            session.rollback()
            return False
        else:
            session.add(candidate_asset)
            session.commit()
            return True

    def del_asset(self, del_user_id, del_ticker):

        session.query(
                Asset
            ).filter_by(
                user_id=del_user_id
            ).filter_by(
                ticker=del_ticker
            ).delete()

        session.commit()

    def edit_t_price(self, edit_user_id, edit_ticker, value):
        """
        Функция принимает ID Юзера, инструмент для изменения и
        новую стоимость, с полученными данными функция изменяет
        таргетную стоимость инструмента в БД
        """
        asset = session.query(
                    Asset
                ).filter_by(
                    user_id=edit_user_id
                ).filter_by(
                    ticker=edit_ticker
                ).first()

        asset.target_price = value
        session.commit()

    def edit_m_price(self, edit_user_id, edit_ticker, value):
        """
        Функция принимает ID Юзера, инструмент для изменения и
        новую стоимость, с полученными данными функция изменяет
        минимальную стоимость инструмента в БД
        """
        asset = session.query(
                Asset
            ).filter_by(
                user_id=edit_user_id
            ).filter_by(
                ticker=edit_ticker
            ).scalar()

        asset.min_price = value
        session.commit()

    def get_user_assets(self, query_user_id, classic_asset=True):
        """
        Функция получает из ДБ все активы пользователя
        и упаковывает их во вложенный список.
        """
        user_assets = session.query(
                Asset
            ).filter(
                Asset.user_id == query_user_id
            ).all()

        packed_assets = []

        for elem in user_assets:
            packed_assets.append([
                elem.ticker,
                elem.add_date,
                elem.initial_price,
                elem.target_price,
                elem.min_price,
                elem.is_crypto
            ])
        if classic_asset:
            packed_assets = [asset for asset in packed_assets if asset[5] is False]
            return packed_assets
        else:
            packed_assets = [asset for asset in packed_assets if asset[5] is True]
            return packed_assets

    def get_polling_data(self, is_crypto):
        """
        Функция получает из ДБ все активы всех пользователей
        и возвращает список следующего содержимого.
        Формирует список в зависимости от атрибута is_crypto.
        [[user_id, ticker, target_price, min_price],...]
        """

        packed_assets = []
        if is_crypto:
            assets = session.query(Asset).filter(Asset.is_crypto == True).all()
            for elem in assets:
                packed_assets.append([
                    elem.user_id,
                    elem.ticker,
                    elem.target_price,
                    elem.min_price
                ])
        else:
            assets = session.query(Asset).filter(Asset.is_crypto == False).all()
            for elem in assets:
                packed_assets.append([
                    elem.user_id,
                    elem.ticker,
                    elem.target_price,
                    elem.min_price
                ])
        return packed_assets
