from settings import DB_CONNECT
from sqlalchemy import create_engine


# engine = sqlalchemy.create_engine('postgresql:///atbdb')
# connection = engine.connect()
# metadata = sqlalchemy.MetaData()


class DbUtils:
    db_string = DB_CONNECT

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
                   "add_date boolean, initial_price float, "
                   "target_price float, min_price float)")

    def addUser(self, id, user_id, shares_user,
                crypto_user, analytics_subscription,
                post_frequency, analytics_frequency, api_key):

        db = create_engine(self.db_string)

        db.execute("INSERT INTO users(id, user_id, shares_user, crypto_user, "
                   "analytics_subscription, post_frequency, "
                   "analytics_frequency, api_key) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", id, user_id,
                   shares_user, crypto_user, analytics_subscription,
                   post_frequency, analytics_frequency, api_key)

    def getUsers(self):
        db = create_engine(self.db_string)
        users = db.execute("SELECT * FROM users")
        return users


# can = DbUtils()
# can.InitTables()
# can.addUser(1,123123,True,True,True,1,2,"somekey")
# users = can.getUsers()
# for user in users:
#     print(user)

'''
class Users(db.Model):
    id = db.Column(db.int)
    user_id = db.Column(db.bigint)
    shares_user = db.Column(db.boolean)
    crypto_user = db.Column(db.boolean)
    analytics_subscription = db.Column(db.boolean)
    post_frequency = db.Column(db.int)
    analytics_frequency = db.Column(db.int)
    api_key = db.Column(db.text)


class Assets(db.Model):
    id = db.Column(db.int)
    user_id = db.Column(db.bigint)
    ticker = db.Column(db.text)
    is_crypto = db.Column(db.boolean)
    add_date = db.Column(db.date)
    initial_price = db.Column(db.float)
    target_price = db.Column(db.float)
    min_price = db.Column(db.float)
'''
