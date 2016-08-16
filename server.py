import os
import pdb
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from model import User, Venue, Visit, connect_to_db, db
from yelp_backend import *
from uber_backend import *

app = Flask(__name__)
app.secret_key = "secretkeysecret"

uber_auth_flow = AuthorizationCodeGrant(
    os.environ['uber_client_id'],
    ['request'],
    os.environ['uber_client_secret'],
    'http://localhost:5000/callback',
    )

@app.route('/')
def index():
    """Homepage"""

    # checks to see if user logged in; redirects to login if not
    if 'user_id' in session:
        return render_template('index.html')
    else:
        flash('Please log in.')
        return redirect('/login')


################################################
# User management routes

@app.route('/login')
def login():
    """Provides user login form"""

    # checks to see if user logged in; redirect to homepage if so
    if 'user_id' in session:
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/login_submit', methods=['POST'])
def submit_login():
    # gets user email and pw from login form
    email = request.form.get('email')
    password = request.form.get('password')

    # retrieves user object from database
    user = User.query.filter_by(email=email).first()
    if user == None:
        flash("Uh-oh, we couldn't find you. Please register.")
        return redirect('/login')
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
    # TODO: Add error handling for duplicate email
    # TODO: Form validation
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


@app.route('/logout')
def logout():
    """Logs user out and removes session"""

    # removes user session and confirms user logout
    del session['user_id']
    flash('You are now logged out.')
    return redirect('/login')


################################################
# App functionality routes

@app.route('/setup_for_departure', methods=['POST'])
def get_user_authorization():

    url = get_user_auth(uber_auth_flow)

    return redirect(url)


@app.route('/callback')
def send_user_to_destination():
    # fetch destination venue from yelp
    end = search_yelp()

    # geocode the user's location input
    start = get_start_coordinates()

    code = request.args.get('code')
    state = request.args.get('state')


    request_ride(start[0], start[1], end[0], end[1], code, state, uber_auth_flow)
    return render_template('index.html')



@app.route('/history')
def history():
    """User view of their complete venue visit history"""
    # add user visit query here
    if 'user_id' in session:
        visits = db.session.query(Venue.name,
            Visit.visited_at).filter(User.user_id==session['user_id']).all()
 
        return render_template('visit-history.html', visits=visits)

    else:
        return render_template('login.html')



if __name__ == '__main__':
   
    app.debug = True
   
    connect_to_db(app)
   
    # DebugToolbarExtension(app)

    # app.run(host='0.0.0.0')
    app.run()
