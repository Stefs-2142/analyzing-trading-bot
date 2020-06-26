from base import Session, Engine, Base
from models import User, Asset
from collections import namedtuple


Base.metadata.create_all(Engine)

# def add_user(user_data):
#     session = Session()
#     
#     users = session.query(User).all()
#     
#     if not [user for user in users if user.user_id == user_data[0]]:
#         session.add(User(*user_data))
#         session.commit()
#         return True
#     else:
#         session.close()
#         return False


# def add_asset(asset_data):
#     session = Session()
#     
#     assets = session.query(Asset).all()
#     
#     if not [asset for asset in assets if asset.user_id == asset_data[0] and asset.ticker == asset_data[1]]:
#         session.add(Asset(*asset_data))
#         session.commit()
#         return True
#     else:
#         session.close()
#         return False        
 
 
#usr = Users([33332,False,True,True,1,2,"somekey"])
   

   
#usr = User(user_id = '333', shares_user = True, crypto_user = True, analytics_subscription = False, post_frequency = 123, analytics_frequency = 333, api_key = '123123')   
#session.add(usr)

usr = User()

print(usr.add_user([35363,False,True,True,1,2,"somekey"]))

# print(usr.del_user(33332))

asst = Asset()


print(asst.add_asset([5151,"TATN",False,'2001-09-28',5.2,6.7,4.2]))

asst.del_asset(5151, 'SBERB')


session = Session() 

users = session.query(User).all()
for user in users:
    print(user.user_id)

print('\r\n')
users = session.query(Asset).all()
for user in users:
    print(user.user_id, user.ticker)

    
    
#User.add_user()
 

#print(usr.())            
        
# print(add_user([33332,False,True,True,1,2,"somekey"]))
# print(add_asset([24124,"RSTI",False,'2001-09-28',5.2,6.7,4.2]))    
# 
# session = Session()
# users = session.query(User).all()
# assets = session.query(Asset).all()
# 
# for asset in assets:
#     print(asset.user_id, asset.ticker)

