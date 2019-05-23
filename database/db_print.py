
from db_session import *


def main():

	# get the lists
	categories = db_session.query(Category).all()
	items = db_session.query(Item).all()

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
