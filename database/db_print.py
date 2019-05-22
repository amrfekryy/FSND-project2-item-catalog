
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Item


def main():
	# bind to db and tables
	engine = create_engine('sqlite:///item_catalog.db')
	Base.metadata.bind = engine

	# establish session connection
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	# get the lists
	categories = session.query(Category).all()
	items = session.query(Item).all()

	print()

	if not categories and not items:
		print("Database is empty")
	else:
		print("Database contents:\n")
		for index, category in enumerate(categories):
			print(f"{index+1}- {category.name}:")
			for index2, item in enumerate(category.items):
				print(f"  {index2+1}- {item.name}")
	print()


if __name__ == '__main__':
	main()
