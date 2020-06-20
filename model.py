from settings import DB_CONNECT
from sqlalchemy import create_engine


class DbUtils:
    db_string = DB_CONNECT

    def DropTables(self):
        db = create_engine(self.db_string)

        db.execute("DROP TABLE users, assets")

    def InitTables(self):
        db = create_engine(self.db_string)

        db.execute("CREATE TABLE IF NOT EXISTS "
                   "users (id int, user_id bigint, "
                   "shares_user boolean, crypto_user boolean, "
                   "analytics_subscription boolean, post_frequency int, "
                   "analytics_frequency int, api_key text)")

        db.execute("CREATE TABLE IF NOT EXISTS "
                   "assets (id int, user_id bigint, "
                   "ticker text, is_crypto boolean, "
                   "add_date date, initial_price float, "
                   "target_price float, min_price float)")

    def AddUser(self, id, user_id, shares_user,
                crypto_user, analytics_subscription,
                post_frequency, analytics_frequency, api_key):

        db = create_engine(self.db_string)

        db.execute("INSERT INTO users(id, user_id, shares_user, crypto_user, "
                   "analytics_subscription, post_frequency, "
                   "analytics_frequency, api_key) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", id, user_id,
                   shares_user, crypto_user, analytics_subscription,
                   post_frequency, analytics_frequency, api_key)

    def AddAsset(self, id, user_id, ticker,
                 is_crypto, add_date, initial_price,
                 target_price, min_price):

        db = create_engine(self.db_string)

        db.execute("INSERT INTO assets(id, user_id, ticker, "
                   "is_crypto, add_date, initial_price, "
                   "target_price, min_price) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   id, user_id, ticker,
                   is_crypto, add_date, initial_price,
                   target_price, min_price)

    def DeleteUser(self, user_id):
        db = create_engine(self.db_string)

        db.execute(f"DELETE FROM users WHERE user_id = {user_id}")

    def DeleteAsset(self, user_id, ticker):
        db = create_engine(self.db_string)

        db.execute("DELETE FROM assets WHERE "
                   f"user_id = {user_id} AND ticker = '{ticker}'")

    def GetUserAssets(self, user_id):
        db = create_engine(self.db_string)

        assets = db.execute(f"SELECT * FROM assets WHERE user_id = {user_id}")

        return assets

    def GetSharesUsers(self):
        db = create_engine(self.db_string)

        users = db.execute("SELECT * FROM users WHERE shares_user = True")

        return users

    def GetCryptoUsers(self):
        db = create_engine(self.db_string)

        users = db.execute("SELECT * FROM users WHERE crypto_user = True")

        return users

    def GetAnalyticsUsers(self):
        db = create_engine(self.db_string)

        users = db.execute("SELECT * FROM users WHERE "
                           "analytics_subscription = True")

        return users

    def GetUsers(self):
        db = create_engine(self.db_string)

        users = db.execute("SELECT * FROM users")

        return users

    def GetAssets(self):
        db = create_engine(self.db_string)

        assets = db.execute("SELECT * FROM assets")

        return assets

    def EditUser(self, user_id, field, variable):
        db = create_engine(self.db_string)

        if field == 'api_key':
            assets = db.execute(f"UPDATE users SET {field} = '{variable}'"
                                f" WHERE user_id = {user_id}")
        else:
            assets = db.execute(f"UPDATE users SET {field} = {variable}"
                                f" WHERE user_id = {user_id}")

    def EditAsset(self, user_id, ticker, field, variable):
        db = create_engine(self.db_string)

        db.execute(f"UPDATE assets SET {field} = {variable}"
                   f" WHERE user_id = {user_id} and ticker = '{ticker}'")


# can = DbUtils()
# can.DropTables()
# can.InitTables()
