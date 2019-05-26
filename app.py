
# flask
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, session as login_session)
# general
import random
import string
import json
import requests
from oauth2client import client
from functools import wraps
# database
# add database directory to python modules path.
import sys
sys.path.append("./database/")
from db_session import *


app = Flask(__name__)


# clear db session after each request
# https://stackoverflow.com/a/34010159
# https://stackoverflow.com/q/30521112
@app.teardown_request
def remove_session(ex=None):
    db_session.remove()


# LOGIN MANAGEMENT

# get google's client id from external json file
file = 'g_client_secrets.json'
G_CLIENT_ID = json.loads(open(file, 'r').read())['web']['client_id']


@app.route('/login/')
def login():
    # create anti-forgery state token
    AZ09 = string.ascii_uppercase + string.digits
    state_token = ''.join(random.choice(AZ09) for x in range(32))
    login_session['state_token'] = state_token
    return render_template('login.html', state_token=state_token)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Check state_token to protect against CSRF
    if request.args.get('state_token') != login_session['state_token']:
        return jsonify('Invalid state token parameter'), 401

    # Check user is already logged in
    if login_session.get('user_id'):
        return jsonify('Current user is already connected.'), 200

    # Collect one-time-auth-code from request
    auth_code = request.data

    # Exchange auth code for credentials obj (access tok, refresh tok, ID tok)
    try:
        ggl_api = 'https://www.googleapis.com/auth/drive.appdata'
        credentials_obj = client.credentials_from_clientsecrets_and_code(
            'g_client_secrets.json',
            [ggl_api, 'profile', 'email'],
            auth_code)
        # print(f"ACCESS TOKEN = {credentials_obj.access_token}")
    except client.FlowExchangeError:
        return jsonify('Failed to upgrade the authorization code'), 401

    # get token information from access token:
    r = requests.get(
        url="https://www.googleapis.com/oauth2/v1/tokeninfo",
        params={'access_token': credentials_obj.access_token})
    token_info = r.json()
    # Verify access token is valid
    if token_info.get('error'):
        return jsonify(token_info.get('error')), 500
    # Verify access token is used for the intended user.
    user_id_from_credentials = credentials_obj.id_token['sub']
    if token_info.get('user_id') != user_id_from_credentials:
        return jsonify("Token's user ID doesn't match given user ID."), 401
    # Verify access token is valid for this app.
    if token_info.get('issued_to') != G_CLIENT_ID:
        return jsonify("Token's client ID does not match app's."), 401

    # Access token tests passed:
    # Store credentials in session for later use.
    login_session['auth_provider'] = 'google'
    login_session['access_token'] = credentials_obj.access_token
    login_session['username'] = credentials_obj.id_token['name']
    login_session['picture'] = credentials_obj.id_token['picture']
    login_session['email'] = credentials_obj.id_token['email']

    # Create new user if not existant
    email = login_session['email']
    user = db_session.query(User).filter_by(email=email).first()
    if not user:
        new_user = User(
            name=login_session['username'],
            email=login_session['email'],
            picture=login_session['picture'])
        db_session.add(new_user)
        db_session.commit()
        user = db_session.query(User).filter_by(email=email).first()
    login_session['user_id'] = user.id

    flash(f"You are now logged in as {login_session['username']}", "success")

    # return successful response to client-side ajax request
    return f"""
        <h1>Welcome, {login_session['username']}!</h1>
        <img src="{login_session['picture']}"
             style="width:60px; height:60px; border-radius:30px;
             -webkit-border-radius:30px; -moz-border-radius:30px;">
    """


@app.route('/gdisconnect')
def gdisconnect():

    # Check user is not logged in
    if not login_session.get('user_id'):
        return jsonify('Current user not connected.'), 401

    # revoke access token
    # see https://developers.google.com/identity/protocols/OAuth2WebServer
    r = requests.post(
        url='https://accounts.google.com/o/oauth2/revoke',
        params={'token': login_session.get('access_token')},
        headers={'content-type': 'application/x-www-form-urlencoded'})
    # successful disconnect returns 200 OK status code
    if r.status_code == 200:
        login_session.clear()  # https://stackoverflow.com/q/27747578
        flash("You have logged out successfully", "success")
        return redirect(url_for('index'))
    else:
        return jsonify('Failed to revoke token for given user.'), 400


# HTML ENDPOINTS

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not login_session.get('user_id'):
            flash("The requested URL requires login", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/catalog/')
def index():
    categories = db_session.query(Category).all()
    return render_template('index.html', categories=categories)


@app.route('/categories/add/', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        # get form inputs
        category_name = request.form.get('category_name')
        # verify form inputs
        if not category_name:
            flash("Category name was not provided", "danger")
            return redirect(url_for('add_category'))
        # create new category
        new_category = Category(name=category_name)
        db_session.add(new_category)
        db_session.commit()
        flash(f"Category <i>{category_name}</i> has been added", "success")
        return redirect(url_for('index'))
    else:
        return render_template('add_category.html')


@app.route('/categories/<int:category_id>/rename/', methods=['GET', 'POST'])
@login_required
def rename_category(category_id):
    category = db_session.query(Category).filter_by(id=category_id).first()
    if request.method == 'POST':
        # get form inputs
        category_new_name = request.form.get('category_new_name')
        # verify inputs
        if not category_new_name:
            flash("Category new name was not provided", "danger")
            return redirect(
                url_for('rename_category', category_id=category_id))
        # update category
        category.name = category_new_name
        db_session.add(category)
        db_session.commit()
        flash(f"Category <i>{category.name}</i> has been renamed", "success")
        return redirect(url_for('index'))
    else:
        return render_template('rename_category.html', category=category)


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    category = db_session.query(Category).filter_by(id=category_id).first()
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
            flash(f"Category <i>{category.name}</i> has been deleted",
                  "success")
        return redirect(url_for('index'))
    else:
        return render_template('delete_category.html', category=category)


@app.route('/categories/<int:category_id>/items/add/', methods=['GET', 'POST'])
@login_required
def add_item(category_id):
    category = db_session.query(Category).filter_by(id=category_id).first()
    if request.method == 'POST':
        # get form inputs
        item_name = request.form.get('item_name')
        item_description = request.form.get('item_description')
        # verify inputs
        if not item_name:
            flash("Item name was not provided", "danger")
            return redirect(url_for('add_item', category_id=category_id))
        if not item_description:
            item_description = "No description yet"
        # create new item
        new_item = Item(
            name=item_name,
            description=item_description,
            category_id=category_id)
        db_session.add(new_item)
        db_session.commit()
        flash(f"Item <i>{new_item.name}</i> has been added", "success")
        return redirect(url_for('index'))
    else:
        return render_template('add_item.html', category=category)


@app.route('/items/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = db_session.query(Item).filter_by(id=item_id).first()
    if request.method == 'POST':
        # get form inputs
        item_new_name = request.form.get('item_new_name')
        item_new_description = request.form.get('item_new_description')
        # verify inputs
        if not (item_new_name or item_new_description):
            flash("No inputs were provided", "danger")
            return redirect(url_for('edit_item', item_id=item_id))
        # update item
        if item_new_name:
            item.name = item_new_name
        if item_new_description:
            item.description = item_new_description
        db_session.add(item)
        db_session.commit()
        flash(f"Item <i>{item.name}</i> has been updated", "success")
        return redirect(url_for('index'))
    else:
        return render_template('edit_item.html', item=item)


@app.route('/items/<int:item_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = db_session.query(Item).filter_by(id=item_id).first()
    if request.method == 'POST':
        # get form inputs
        answer = request.form.get('answer')
        # verify answer
        if answer == 'yes':
            # delete item
            db_session.delete(item)
            db_session.commit()
            flash(f"Item <i>{item.name}</i> has been deleted", "success")
        return redirect(url_for('index'))
    else:
        return render_template('delete_item.html', item=item)


@app.route('/api/')
def api_docs():
    return render_template('api_docs.html')


# API ENDPOINTS

@app.route('/api/categories')
def api_categories():
    categories = db_session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/api/category/<int:category_id>')
def api_category(category_id):
    category = db_session.query(Category).filter_by(id=category_id).first()
    if not category:
        return f"There is no category with id {category_id}"

    items_list = []
    for item in category.items:
        items_list.append({'item_id': item.id, 'item_name': item.name})

    return jsonify(
        category_id=category.id,
        category_name=category.name,
        category_items=items_list)


@app.route('/api/item/<int:item_id>')
def api_item(item_id):
    item = db_session.query(Item).filter_by(id=item_id).first()
    if not item:
        return f"There is no item with id {item_id}"

    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
