from base import Session, Engine, Base
from model import User, Asset

Base.metadata.create_all(Engine)

def add_user(user_data):
    session = Session()
    
    users = session.query(User).all()
    
    if not [user for user in users if user.user_id == user_data[0]]:
        session.add(User(*user_data))
        session.commit()
        return True
    else:
        session.close()
        return False


def add_asset(asset_data):
    session = Session()
    
    assets = session.query(Asset).all()
    
    if not [asset for asset in assets if asset.user_id == asset_data[0] and asset.ticker == asset_data[1]]:
        session.add(Asset(*asset_data))
        session.commit()
        return True
    else:
        session.close()
        return False        
        
        
print(add_user([33332,False,True,True,1,2,"somekey"]))
print(add_asset([24124,"RSTI",False,'2001-09-28',5.2,6.7,4.2]))    

session = Session()
users = session.query(User).all()
assets = session.query(Asset).all()

for asset in assets:
    print(asset.user_id, asset.ticker)

