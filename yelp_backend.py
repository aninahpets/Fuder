import os
import pdb
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from model import User, Venue, Visit, connect_to_db, db
from random import randrange
import requests
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

def search_yelp():
    """Uses Yelp API v3 to fetch venue; creates venue and visit records"""
    # retrieve user's address and create dict with search params
    user_location = request.args.get('user-address')

    resp = requests.post("https://api.yelp.com/oauth2/token",
                         data={'grant_type': 'client_credentials',
                               'client_id': os.environ['yelp_app_id'],
                               'client_secret': os.environ['yelp_app_secret']})

    yelp_access_token = resp.json()['access_token']

    results = requests.get('https://api.yelp.com/v3/businesses/search?location=%s&sort_by=rating&categories=restaurants&open_now_filter=True' % user_location,
        headers={'Authorization': 'Bearer %s' % yelp_access_token})

    results = results.json()
    
    # selecting the business to which we will send the user
    optionsnumber = randrange(len(results['businesses']))

    # extracting data from json
    destination = {'name': results['businesses'][optionsnumber]['name'],
        'id': results['businesses'][optionsnumber]['id'],
        'latitude': results['businesses'][optionsnumber]['coordinates']['latitude'],
        'longitude': results['businesses'][optionsnumber]['coordinates']['longitude']}

   # checks to see if the venue exists in the database and creates a visit record
    match = db.session.query(Venue).filter_by(venue_id=destination['id']).first()

    if match:
        new_visit = Visit(user_id=session['user_id'],
                            venue_id=destination['id'])
        db.session.add(new_visit)
        db.session.commit()

    else:
        new_venue = Venue(venue_id=destination['id'],
                            name=destination['name'],
                            latitude=destination['latitude'],
                            longitude=destination['longitude'])
        db.session.add(new_venue)
        db.session.commit()

        new_visit = Visit(user_id=session['user_id'],
                            venue_id=destination['id'])
        db.session.add(new_visit)
        db.session.commit()

    end_latitude = destination['latitude']
    end_longitude = destination['longitude']

    return (user_location, end_latitude, end_longitude)

