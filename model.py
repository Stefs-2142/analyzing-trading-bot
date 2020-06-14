import sqlalchemy


db = sqlalchemy.create_engine('postgresql:///atbDB.db')


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
