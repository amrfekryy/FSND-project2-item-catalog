# add database directory to python modules path.
import sys
sys.path.append("./database/")

from flask import (
	Flask, render_template, request, redirect,
	url_for)
from db_session import *

app = Flask(__name__)


# clear db session after each request
# https://stackoverflow.com/a/34010159
# https://stackoverflow.com/q/30521112
@app.teardown_request
def remove_session(ex=None):
    db_session.remove()


@app.route('/')
@app.route('/catalog/')
def index():
	categories = db_session.query(Category).all()
	return render_template('index.html', categories=categories)


@app.route('/categories/add/', methods=['GET', 'POST'])
def add_category():
	if request.method == 'POST':
		# get form inputs
		category_name = request.form.get('category_name')
		# verify form inputs
		if not category_name:
			return "Category name was not provided"
		# create new category
		new_category = Category(name=category_name)
		db_session.add(new_category)
		db_session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('add_category.html')


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def category_items(category_id):
	return f"A list of items that belong to category with id {category_id}"


@app.route('/categories/<int:category_id>/rename/', methods=['GET', 'POST'])
def rename_category(category_id):
	category = db_session.query(Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		# get form inputs
		category_new_name = request.form.get('category_new_name')
		# verify inputs
		if not category_new_name:
			return "Category new name was not provided"
		# update category
		category.name = category_new_name
		db_session.add(category)
		db_session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('rename_category.html', category=category)


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
	category = db_session.query(Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		# get form inputs
		answer = request.form.get('answer')
		# verify answer
		if answer == 'yes':
			# delete category and its items
			for item in category.items:
				db_session.delete(item)
			db_session.delete(category)
			db_session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('delete_category.html', category=category)


@app.route('/categories/<int:category_id>/items/add/', methods=['GET', 'POST'])
def add_item(category_id):
	if request.method == 'POST':
		# get form inputs
		item_name = request.form.get('item_name')
		item_description = request.form.get('item_description')
		# verify inputs
		if not item_name:
			return "Item name was not provided"
		if not item_description:
			item_description = "No description yet"
		# create new item
		new_item = Item(
			name=item_name,
			description=item_description,
			category_id=category_id)
		db_session.add(new_item)
		db_session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('add_item.html', category_id=category_id)


@app.route('/items/<int:item_id>/')
def item_info(item_id):
	return f"Description of item with id {item_id}"


@app.route('/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(item_id):
	item = db_session.query(Item).filter_by(id=item_id).one()
	if request.method == 'POST':
		# get form inputs
		item_new_name = request.form.get('item_new_name')
		item_new_description = request.form.get('item_new_description')
		# verify inputs
		if not (item_new_name or item_new_description):
			return "No inputs were provided"
		# update item
		if item_new_name: item.name = item_new_name
		if item_new_description: item.description = item_new_description
		db_session.add(item)
		db_session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('edit_item.html', item=item)


@app.route('/items/<int:item_id>/delete/')
def delete_item(item_id):
	return f"A form for deleting item with id {item_id}"



if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
