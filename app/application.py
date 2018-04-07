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
from models import Base, User


app = Flask(__name__)


APPLICATION_NAME = "My Bookkeeping App"


# Connect to Database and create database session
engine = create_engine('sqlite:///userAccountingLedger.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def showRestaurants():
    return render_template('main.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
