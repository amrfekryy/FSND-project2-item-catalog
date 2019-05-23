
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from db_setup import Base, Category, Item

# bind to db and tables
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

# establish session connection
db_session = scoped_session(sessionmaker(bind=engine))
