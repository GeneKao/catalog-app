#!/usr/bin/env python3

""" My bookkeeping app

"""

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao.gene@gmail.com"


from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash, make_response)
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Project, Ledger_Item

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests


app = Flask(__name__)


APPLICATION_NAME = "My Bookkeeping App"
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///userAccountingLedger.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
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
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    # Render the login template
    return render_template('login.html', STATE=state)


# JSON APIs to view Project Information
@app.route('/project/<int:project_id>/ledger/JSON')
def projectMenuJSON(project_id):
    project = session.query(Project).filter_by(id=project_id).one()
    items = session.query(Ledger_Item).filter_by(
        project_id=project_id).all()
    return jsonify(Ledgers=[i.serialize for i in items])


@app.route('/project/<int:project_id>/ledger/<int:ledger_id>/JSON')
def ledgerItemJSON(project_id, ledger_id):
    Ledger_Item = session.query(Ledger_Item).filter_by(id=ledger_id).one()
    return jsonify(Ledger_Item=Ledger_Item.serialize)


@app.route('/project/JSON')
def projectJSON():
    projects = session.query(Project).all()
    return jsonify(projects=[r.serialize for r in projects])


# Show all projects
@app.route('/')
@app.route('/project/')
def showProjects():
    projects = session.query(Project).order_by(asc(Project.name))
    return render_template('projects.html', projects=projects)


# Create a new project
@app.route('/project/new/', methods=['GET', 'POST'])
def newProject():
    if request.method == 'POST':
        newProject = Project(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newProject)
        flash('New Project %s Successfully Created' % newProject.name)
        session.commit()
        return redirect(url_for('showProjects'))
    else:
        return render_template('newProject.html')


# Edit a project
@app.route('/project/<int:project_id>/edit/', methods=['GET', 'POST'])
def editProject(project_id):
    editedProject = session.query(
        Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedProject.name = request.form['name']
            flash('Project Successfully Edited %s' % editedProject.name)
            return redirect(url_for('showProjects'))
    else:
        return render_template('editProject.html', project=editedProject)


# Delete a project
@app.route('/project/<int:project_id>/delete/', methods=['GET', 'POST'])
def deleteProject(project_id):
    projectToDelete = session.query(
        Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        session.delete(projectToDelete)
        flash('%s Successfully Deleted' % projectToDelete.name)
        session.commit()
        return redirect(url_for('showProjects', project_id=project_id))
    else:
        return render_template('deleteProject.html', project=projectToDelete)


# Show a project ledger
@app.route('/project/<int:project_id>/')
@app.route('/project/<int:project_id>/ledger/')
def showLedger(project_id):
    project = session.query(Project).filter_by(id=project_id).one()
    creator = getUserInfo(project.user_id)
    items = session.query(Ledger_Item).filter_by(
        project_id=project_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicledger.html', items=items, project=project, creator=creator)
    else:
        return render_template('ledger.html', items=items, project=project, creator=creator)


# Create a new ledger item
@app.route('/project/<int:project_id>/ledger/new/', methods=['GET', 'POST'])
def newLedgerItem(project_id):
    project = session.query(Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        newItem = Ledger_Item(name=request.form['name'], description=request.form['description'],
                              types=request.form['types'], cost=request.form['cost'],
                              project_id=project_id, user_id=project.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showLedger', project_id=project_id))
    else:
        return render_template('newLedgerItem.html', project_id=project_id)


# Edit a ledger item
@app.route('/project/<int:project_id>/ledger/<int:ledger_id>/edit', methods=['GET', 'POST'])
def editLedgerItem(project_id, ledger_id):

    editedItem = session.query(Ledger_Item).filter_by(id=ledger_id).one()
    project = session.query(Project).filter_by(id=project_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
            session.add(editedItem)
            session.commit()
            flash('Menu Item Successfully Edited')
        return redirect(url_for('showLedger', project_id=project_id))
    else:
        return render_template('editLedgerItem.html', project_id=project_id, ledger_id=ledger_id, item=editedItem)


# Delete a ledger item
@app.route('/project/<int:project_id>/ledger/<int:ledger_id>/delete', methods=['GET', 'POST'])
def deleteLedgerItem(project_id, ledger_id):
    project = session.query(Project).filter_by(id=project_id).one()
    itemToDelete = session.query(Ledger_Item).filter_by(id=ledger_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showLedger', project_id=project_id))
    else:
        return render_template('deleteLedgerItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
