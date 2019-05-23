
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Item

# bind to db and tables
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

# establish session connection
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
