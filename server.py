import os
import bcrypt
import json
import pdb
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from model import User, Venue, Visit, connect_to_db, db
from helper_functions import *

app = Flask(__name__)
app.secret_key = 'secret_key'

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
    google_api_key = os.environ['google_api_key']
    # checks to see if user logged in; redirects to login if not
    if User.user_logged_in():
        return render_template('index.html', google_api_key=google_api_key)
    else:
        flash('Please log in.')
        return redirect('/login')

# @app.route('/status')
# def get_status():
#     if 'count' in session:
#         session['count'] = session['count'] + 1
#     else:
#         session['count'] = 0
#     return jsonify({'count': session['count']})

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
    if User.log_user_in(email, password):
        return redirect('/')
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    """Registers user as a user of the app."""
    # TODO: Add error handling for duplicate email
    # TODO: Form validation
    email = request.form.get('email')
    password = request.form.get('password')
    User.create_user(email, password)

    return redirect('/')


@app.route('/logout')
def logout():
    """Logs user out of app."""
    User.log_user_out()
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
    price = request.form.getlist('price')
    category = request.form.get('venue-option')
    price, category = create_yelp_price_cat_params(price, category)
    start = get_start_coordinates(user_location)

    # fetch destination venue from Yelp using start coordinates
    # create a visit record in the database with start/end coordinates
    results = search_yelp(start[0], start[1], category, price)
    # redirect user if Yelp didn't return any results matching their request
    if not results['businesses']:
        flash("Uh-oh, we couldn't find anywhere to take you. Please try \
            narrowing your search a little!")
        return redirect('/')
    else:
        process_yelp_results(results, start[0], start[1])

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
    coordinates, city = Visit.get_uber_ride_params()
    # request a ride on behalf of the user
    request_uber_ride(coordinates[0], coordinates[1], coordinates[2], 
                        coordinates[3], uber_auth_flow, code, state)
    flash('Uber will be taking you to a mystery destination in %s!' % city)
    return redirect('/waiting')


@app.route('/get_options.json')
def provide_options():
    ven_type = request.args.get('venue-type')
    if ven_type == 'bar':
        options = {'Cocktail Bar': 'cocktailbars', 'Dive Bar': 'divebars',
                'Gay Bar': 'gaybars', 'Pub': 'pubs', 'Sports Bar': 'sportsbars',
                'Tiki Bar': 'tikibars', 'Wine Bar': 'wine_bars'}
    else:
        options = {'African': 'african', 'American': 'tradamerican', 'Barbeque':
         'bbq', 'Bistro': 'bistros', 'Burgers': 'burgers', 'Cajun': 'cajun', 
         'Chinese': 'chinese', 'Cuban': 'cuban', 'Diner': 'diners', 'Ethiopian':
          'ethiopian', 'French': 'french', 'German': 'german', 'Greek': 'greek',
           'Indian': 'indian', 'Italian': 'italian', 'Japanese': 'japanese', 
           'Korean': 'korean', 'Mexican': 'mexican', 'Pizza': 'pizza',
           'Tapas': 'tapasmallplates', 'Thai': 'thai', 'Vegan': 'vegan'}
    return jsonify(options)

@app.route('/waiting')
def get_uber_ride_status():
    # get_uber_status()
    # TODO: jsonify uber status and return to AJAX, which will continue to poll
    # return rendertemplate when ride is on way and give options to
    # cancel/start over
    return render_template('waiting.html')

@app.route('/get_image_url.json')
def get_image_url():
    image_url = Venue.get_venue_img()
    return jsonify(image_url)

@app.route('/get_history.json')
def history():
    """Provides the user with a complete view of their visit history."""
    visits = User.get_user_visit_history()
    return jsonify(visits)


if __name__ == '__main__': # pragma: no cover
   
    app.debug = True
   
    connect_to_db(app)
   
    # DebugToolbarExtension(app)

    # app.run(host='0.0.0.0')
    app.run()
