from flask import Flask, render_template, request, url_for, redirect, \
                  make_response, flash, jsonify
from flask import session as login_session
from flask_cors import CORS

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database_setup import engine, Base, Category, Person, User

from googleapiclient import discovery
import httplib2
from oauth2client import client

import json
import requests
import random
import string

app = Flask(__name__)
CORS(app)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@app.route('/sign')
def loginOrLogout():
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        return redirect(url_for('googleSignOut'))


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/login/cancel')
def loginCancel():
    return redirect(url_for('showAllCategories'))


@app.route('/signin', methods=['POST'])
def googleAuthenticate():
    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # validate state token
    if request.get_json().get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Receive auth_code by HTTPS POST
    authCode = request.get_json().get('authCode')
    CLIENT_SECRET_FILE = './client_secrets.json'
    CLIENT_ID = json.loads(
                open(CLIENT_SECRET_FILE, 'r').read())['web']['client_id']

    # Exchange auth code for access token, refresh token, and ID token
    try:
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/drive.appdata',
             'profile', 'email'],
            authCode)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_auth_id = credentials.id_token['sub']
    if result['user_id'] != google_auth_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_auth_id = login_session.get('google_auth_id')
    if stored_access_token is not None and \
            google_auth_id == stored_google_auth_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_auth_id'] = google_auth_id
    login_session['email'] = credentials.id_token['email']

    # See if a user exists, if it doesn't make a new one
    userId = getUserID(login_session['email'])
    if not userId:
        userId = createUser(login_session)
    login_session['user_id'] = userId

    response = make_response(
        json.dumps("Login Successful"), 200)
    # print "Login Successful"
    response.headers['Content-Type'] = 'application/json'
    return response


def createUser(login_session):
    newUser = User(email=login_session['email'])
    Session.add(newUser)
    Session.commit()
    user = Session.query(User).filter_by(email=login_session['email']).one()
    Session.remove()
    return user.id


def getUserInfo(user_id):
    user = Session.query(User).filter_by(id=user_id).one()
    Session.remove()
    return user


def getUserID(email):
    try:
        user = Session.query(User).filter_by(email=email).one()
        Session.remove()
        return user.id
    except MultipleResultsFound:
        print "getUserID(): MultipleResultsFound"
    except NoResultFound:
        print "getUserID(): NoResultFound"


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/logout')
def googleSignOut():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        print 'Current user not connected'
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        print('Successfully disconnected')
    else:
        # For whatever reason, the given token was invalid.
        print('Failed to revoke token for given user.')
        print('For whatever reason, the given token was invalid')
    login_session.clear()
    flash("Logged out successfully")
    return redirect(url_for('showAllCategories'))


@app.route('/')
@app.route('/categories/')
def showAllCategories():
    categories = Session.query(Category).order_by(Category.id)
    Session.remove()
    if 'user_id' not in login_session:
        return render_template('public_categories.html', categories=categories)
    else:
        return render_template('categories.html',
                               categories=categories,
                               user_id=login_session['user_id'])


# JSON APIs to view all categories
@app.route('/JSON/')
@app.route('/categories/JSON/')
def showAllCategoriesJSON():
    categories = Session.query(Category).order_by(Category.id)
    Session.remove()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/categories/new/', methods=['GET', 'POST'])
def addCategory():
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        newCategory = Category(name=request.form['category_name'],
                               user_id=login_session['user_id'])
        Session.add(newCategory)
        Session.commit()
        Session.remove()
        flash("Successfully added a new category")
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/category/<string:category_name>/')
def showCategory(category_name):
    category_id = Session.query(Category).filter(
                  Category.name == category_name).one().id
    persons = Session.query(Person).filter(Person.category_id == category_id)
    Session.remove()
    if 'user_id' not in login_session:
        return render_template('public_category.html',
                               category_name=category_name,
                               persons=persons)
    else:
        return render_template('category.html',
                               category_name=category_name,
                               persons=persons,
                               user_id=login_session['user_id'])


@app.route('/category/<string:category_name>/JSON/')
def showCategoryJSON(category_name):
    category_id = Session.query(Category).filter(
                  Category.name == category_name).one().id
    persons = Session.query(Person).filter(Person.category_id == category_id)
    Session.remove()
    return jsonify([person.serialize for person in persons])


@app.route('/category/<string:category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        editedCategory = Session.query(Category).filter(
                         Category.name == category_name).one()
        if request.form['edited_category_name']:
            editedCategory.name = request.form['edited_category_name']
        Session.add(editedCategory)
        Session.commit()
        Session.remove()
        flash("Successfully edited category name")
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('editCategory.html', category_name=category_name)  # NOQA


@app.route('/category/<string:category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    categoryToBeDeleted = Session.query(Category).filter(
                     Category.name == category_name).one()
    if request.method == 'POST':
        Session.delete(categoryToBeDeleted)
        Session.commit()
        Session.remove()
        flash("Successfully deleted the category")
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('deleteCategory.html', category_name=category_name)  # NOQA


@app.route('/category/<string:category_name>/new/', methods=['GET', 'POST'])
def addPerson(category_name):
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if request.form['person_name'] and request.form['mobile']:
            category_id = Session.query(Category).filter(
                          Category.name == category_name).one().id
            newPerson = Person(name=request.form['person_name'],
                               mobile=request.form['mobile'],
                               address=request.form['address'],
                               category_id=category_id,
                               user_id=login_session['user_id'])
            Session.add(newPerson)
            Session.commit()
            Session.remove()
            flash("Successfully added a new entry")
            return redirect(url_for('showCategory', category_name=category_name))  # NOQA
    else:
        return render_template('newPerson.html', category_name=category_name)  # NOQA


@app.route('/category/<string:category_name>/<int:person_id>/edit/',
           methods=['GET', 'POST'])
def editPerson(category_name, person_id):
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    editedPerson = Session.query(Person).filter(
                   Person.id == person_id).one()
    if request.method == 'POST':
        if request.form['person_name'] != editedPerson.name:
            editedPerson.name = request.form['person_name']
        if request.form['mobile'] != editedPerson.mobile:
            editedPerson.mobile = request.form['mobile']
        if request.form['address'] != editedPerson.address:
            editedPerson.address = request.form['address']
        Session.add(editedPerson)
        Session.commit()
        Session.remove()
        flash("Successfully edited the entry")
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('editPerson.html',
                               category_name=category_name,
                               person=editedPerson)


@app.route('/category/<string:category_name>/<int:person_id>/delete/',
           methods=['GET', 'POST'])
def deletePerson(category_name, person_id):
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    personToBeDeleted = Session.query(Person).filter(
                     Person.id == person_id).one()
    if request.method == 'POST':
        Session.delete(personToBeDeleted)
        Session.commit()
        Session.remove()
        flash("Successfully deleted the entry")
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        return render_template('deletePerson.html',
                               category_name=category_name,
                               person_id=person_id)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
