from settings import DB_CONNECT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Engine = create_engine(DB_CONNECT)

Session = sessionmaker(bind=Engine)

session = Session()

Base = declarative_base()
