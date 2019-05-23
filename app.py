# add database directory to python modules path.
import sys
sys.path.append("./database/")

from flask import Flask
from db_session import *

app = Flask(__name__)


# clear db session after each request
# https://stackoverflow.com/a/34010159
# https://stackoverflow.com/q/30521112
@app.teardown_request
def remove_session(ex=None):
    db_session.remove()


@app.route('/')
def index():
	categories = db_session.query(Category).all()
	items = db_session.query(Item).all()

	output = """
		<h1>Categories</h1>
		<ul>
			{}
		</ul>
		<br>
		<h1>Items</h1>
		<ul>
			{}
		</ul>
	"""

	categories_list = ""
	items_list = ""
	
	for category in categories:
		categories_list += f"<li>{category.name}</li>"
	for item in items:
		items_list += f"<li>{item.name}</li>"

	return output.format(categories_list, items_list)


if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
