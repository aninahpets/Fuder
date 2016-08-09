import os
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from model import User, Venue, Visit, connect_to_db, db
from random import choice
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

app = Flask(__name__)
app.secret_key = "secretkeysecret"


@app.route('/')
def index():
    """Homepage"""

    # checks to see if user logged in
    if 'user_id' in session:
        return render_template('index.html')
    else:
        flash('Please log in.')
        return redirect('/login')


@app.route('/login')
def login():
    """Provides user login form"""

    if 'user_id' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/yelp_search')
def search_yelp():
    # using Python os.environ to access environment variables
    yelp_auth = Oauth1Authenticator(
        consumer_key=os.environ['yelp_consumer_key'],
        consumer_secret=os.environ['yelp_consumer_secret'],
        token=os.environ['yelp_token'],
        token_secret=os.environ['yelp_token_secret'])

    # retrieve user's location and create dict with search params
    location = request.args.get('user-address')
    params = {'term': 'restaurant', 'location': location}

    # API call
    client = Client(yelp_auth)
    result = client.search(params)
    return result


@app.route('/login_submit', methods=['POST'])
def submit_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # retrieves user object from database
    user = User.query.filter_by(email=email).one()
    user_id = user.user_id

    # logs current user out if session exists
    if 'user_id' in session:
        del session['user_id']

    # checks for password match and creates new session if successful
    if user.password == password:
        session['user_id'] = user.user_id
        return redirect('/')
    # redirects to login page if unsuccessful
    else:
        flash('Your password was incorrect. Please try again.')
        return redirect('/login')


@app.route('/register', methods=['POST'])
def register():
    # TO DO: Add error handling for duplicate email
    # TO DO: Form validation
    email = request.form.get('email')
    password = request.form.get('password')

    # create new user instance and add to database
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # retrieves newly created user object and creates new session
    user = User.query.filter_by(email=email).one()
    user_id = user.user_id
    session['user_id'] = user.user_id
    return redirect('/')
    

@app.route('/request')
def request_ride():
    """User view while Uber ride request is processing"""

    return render_template('processing.html')


@app.route('/history')
def history():
    """User view of their complete venue visit history"""

    return render_template('visit-history.html')



if __name__ == '__main__':
   
    app.debug = True
   
    connect_to_db(app)
   
    # DebugToolbarExtension(app)

    app.run(host='0.0.0.0')

