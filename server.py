import os
import pdb
import bcrypt
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from model import User, Venue, Visit, connect_to_db, db
from helper_functions import *

app = Flask(__name__)
app.secret_key = "secret_key"

# instantiating AuthorizationCodeGrant object for use with Uber methods
# across the app
uber_auth_flow = AuthorizationCodeGrant(
    os.environ['uber_client_id'],
    ['request'],
    os.environ['uber_client_secret'],
    'http://localhost:5000/callback',
    )


@app.route('/')
def index():
    """Checks for user login and returns homepage or login template."""

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
    """Provides user login form."""

    # checks to see if user logged in; redirect to homepage if so
    if 'user_id' in session:
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/login_submit', methods=['POST'])
def submit_login():
    """Logs user in to app."""
    # gets user email and pw from login form
    email = request.form.get('email')
    password = request.form.get('password')

    # retrieves user object from database
    user = User.query.filter_by(email=email).first()
    if user == None:
        flash("Uh-oh, we couldn't find you. Please register.")
        return redirect('/login')

    # logs current user out if session exists
    if 'user_id' in session:
        del session['user_id']

    # checks for password match and creates new session if successful
    if bcrypt.checkpw(password, user.password):
    # if user.password == password:
        session['user_id'] = user.user_id
        return redirect('/')

    # redirects to login page if unsuccessful
    else:
        flash('Your password was incorrect. Please try again.')
        return redirect('/login')


@app.route('/register', methods=['POST'])
def register():
    """Registers user as a user of the app."""
    # TODO: Add error handling for duplicate email
    # TODO: Form validation
    email = request.form.get('email')
    password = request.form.get('password')

    # hash and salt user pw
    password = bcrypt.hashpw(password, bcrypt.gensalt())

    # create new user record and add to database
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.user_id
    return redirect('/')


@app.route('/logout')
def logout():
    """Logs user out of app."""

    # remove user session and confirm user logout
    del session['user_id']
    flash('You are now logged out.')
    return redirect('/login')


################################################
# App functionality routes

@app.route('/get_user_auth', methods=['POST'])
def get_user_authorization():
    """
    Retrieves user location, creates unique visit record, and redirects user
    to Uber for authorization of app to make ride requests.
    """
    # retrieve user's location from text input and return as start coordinates
    user_location = request.form.get('user-address')
    start = get_start_coordinates(user_location)

    # fetch destination venue from Yelp using start coordinates
    # create a visit record in the database with start/end coordinates
    search_yelp(start[0], start[1])

    # call get_user_auth, passing in uber_auth_flow object and redirect to
    # custom auth URL provided by Uber
    url = get_user_auth(uber_auth_flow)
    return redirect(url)


@app.route('/callback')
def send_user_to_destination():
    """
    Retrieves credentials from Uber callback, retrieves start/end coordinates
    from the database, and requests an Uber on behalf of the user.
    """

    # retrieve code and state from Uber's GET request to /callback route
    code = request.args.get('code')
    state = request.args.get('state')

    # retrieve start and end coordinates from newly created visit record
    coordinates = db.session.query(Visit.start_lat, Visit.start_lng, Visit.end_lat, Visit.end_lng).filter_by(user_id=session['user_id']).order_by('visited_at desc').first()

    # request a ride on behalf of the user
    request_uber_ride(coordinates[0], coordinates[1], coordinates[2], coordinates[3], uber_auth_flow, code, state)
    return render_template('waiting.html')


@app.route('/history')
def history():
    """Provides the user with a complete view of their visit history."""

    if 'user_id' in session:
        # ask in advance for all visit/venue data and add to list of 
        # visits when there is a user match
        visits = []
        raw_visits = Visit.query.options(db.joinedload('venue')).all()
        for visit in raw_visits:
            if visit.user_id==session['user_id']:
                visits.append(visit)
        # pass list of visits to Jinja
        return render_template('visit-history.html', visits=visits)

    else:
        return render_template('login.html')


if __name__ == '__main__':
   
    app.debug = True
   
    connect_to_db(app)
   
    # DebugToolbarExtension(app)

    # app.run(host='0.0.0.0')
    app.run()
