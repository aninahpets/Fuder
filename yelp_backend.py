import os
import pdb
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from model import User, Venue, Visit, connect_to_db, db
from random import randrange
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

def search_yelp():
    # using Python os.environ to access environment variables
    yelp_auth = Oauth1Authenticator(
        consumer_key=os.environ['yelp_consumer_key'],
        consumer_secret=os.environ['yelp_consumer_secret'],
        token=os.environ['yelp_token'],
        token_secret=os.environ['yelp_token_secret'])
    
    # retrieve user's address and create dict with search params
    location = request.args.get('user-address')
    params = {'sort': 2, 'limit': 20, 'category_filter': 'restaurants'}

    # constucting a client (instance of Oauth1Authenticator)
    client = Client(yelp_auth)

    # using client to call API
    result = client.search(location, **params)

    # selecting the business to which we will send the user
    optionsnumber = randrange(len(result.businesses))

    destination = {'name': result.businesses[optionsnumber].name,
        'id': result.businesses[optionsnumber].id,
        'latitude': result.businesses[optionsnumber].location.coordinate.latitude,
        'longitude': result.businesses[optionsnumber].location.coordinate.longitude}

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

    return destination['latitude'], destination['longitude']