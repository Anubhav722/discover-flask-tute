# Flask imports
from flask import Flask, render_template, redirect, url_for, request, session, flash#, g
from flask_sqlalchemy import SQLAlchemy

from functools import wraps

import sqlite3
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
# app.secret_key = 'blah'
# app.database = 'sample.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# CREATE THE SQLALCHEMY OBJECT
db = SQLAlchemy(app)

from models import *


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# HAVE COMMENTED THIS OUT ONCE WE HAVE SEPARATE SQLALCHEMY DB CONFIG
# def connect_db():
#     return sqlite3.connect('posts.db')


# @app.route('/')
# @login_required
# def home():
#     posts = []
#     try:
#         g.db = connect_db()
#         cur = g.db.execute('select * from blog_post')
#         posts = [dict(title=row[1], description=row[2]) for row in cur.fetchall()]
#         g.db.close()
#     except sqlite3.OperationalError:
#         flash("You have no database")
#     return render_template("index.html", posts=posts)


@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", posts=posts)


@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You just logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You logged out')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
