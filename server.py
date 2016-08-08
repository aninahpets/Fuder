import os
from flask import (Flask, render_template, redirect, request, flash, session)
from model import User, Venue, Visit, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

app = Flask(__name__)

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
    """Provides user login"""

    return render_template('login.html')

@app.route('/yelp_search')
def search_yelp():
    # using Python os.environ to access environment variables
    yelp_auth = Oauth1Authenticator(
        consumer_key=os.environ['yelp_consumer_key'],
        consumer_secret=os.environ['yelp_consumer_secret'],
        token=os.environ['yelp_token'],
        token_secret=os.environ['yelp_token_secret'])

    location = request.args.get('user-address')

    params = {'term': 'restaurant', 'location': location}

    client = Client(yelp_auth)
    result = client.search(params)
    return result


@app.route('/submit', methods=['POST'])
def submit_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # checks for existing user in database
    user = User.query.filter_by(email=email).one()
    user_id = user.user_id

    # checks to see if another user is already logged in and logs them out if so
    if 'user_id' in session:
        del session['user_id']

        # checks for password match
        if user.password == password:
            return redirect('/')
        else:
            flash('Your password was incorrect. Please try again.')
            return redirect('/login')


@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('new-email')
    password = request.form.get('new-password')
    

@app.route('/request')
def request():
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

    app.run()

