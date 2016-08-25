import os
import pdb
import googlemaps
import requests
from model import User, Venue, Visit, connect_to_db, db
from random import randrange
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session

def get_start_coordinates(address):
    """Geocode and return user's current location from input string."""

    # Instantiate new Client object gmaps
    gmaps = googlemaps.Client(key=os.environ['google_api_key'])

    # Use gmaps object to geocode user input
    geocode_result = gmaps.geocode('%s' % address)
    coordinates = geocode_result[0]['geometry']['location']
    start_latitude = coordinates['lat']
    start_longitude = coordinates['lng']

    return start_latitude, start_longitude


def get_user_auth(uber_auth_flow):
    """Send user to URL uber_auth_url to authorize app access."""
    
    uber_auth_url = uber_auth_flow.get_authorization_url()

    return uber_auth_url


def request_uber_ride(start_lat, start_lng, end_lat, end_lng, uber_auth_flow, code, state):
    """Send a ride request on behalf of a user."""

    # Instantiate new session & client object and retrieve credentials
    uber_session = uber_auth_flow.get_session('http://0.0.0.0:5000/callback?code=%s&state=%s' % (code, state))
    uber_client = UberRidesClient(uber_session, sandbox_mode=True)
    credentials = uber_session.oauth2credential


    response = uber_client.request_ride(
        start_latitude=start_lat,
        start_longitude=start_lng,
        end_latitude=end_lat,
        end_longitude=end_lng
        )

    ride_details = response.json
    ride_id = ride_details.get('request_id')


def search_yelp(start_lat, start_lng, category, price):
    """
    Use Yelp API v3 to fetch a venue; create venue and visit records in
    database.
    """
   
    # make a request to Yelp's oauth2/token endpoint using app credentials
    resp = requests.post("https://api.yelp.com/oauth2/token",
                         data={'grant_type': 'client_credentials',
                               'client_id': os.environ['yelp_app_id'],
                               'client_secret': os.environ['yelp_app_secret']})

    # retrieve unique access token from Yelp's response
    yelp_access_token = resp.json()['access_token']

    # make a request to Yelp's API with the returned access token using the 
    # start coordinates as search params
    results = requests.get('https://api.yelp.com/v3/businesses/search?latitude=%s&longitude=%s&sort_by=rating&categories=%s&price=%s&open_now_filter=True' % (start_lat, start_lng, category, price),
        headers={'Authorization': 'Bearer %s' % yelp_access_token})

    results = results.json()

    return results
    
def process_yelp_results(results, start_lat, start_lng):
    # select the business to which we will send the user at random
    optionsnumber = randrange(len(results['businesses']))

    # extract necessary data from json results and store in a dict
    destination = {'name': results['businesses'][optionsnumber]['name'],
        'id': results['businesses'][optionsnumber]['id'],
        'latitude': results['businesses'][optionsnumber]['coordinates']['latitude'],
        'longitude': results['businesses'][optionsnumber]['coordinates']['longitude']}


    # check to see if the venue exists in the database (create a venue record
    # if not) and create a visit record
    match = db.session.query(Venue).filter_by(venue_id=destination['id']).first()

    if match:
        new_visit = Visit(user_id=session['user_id'],
                            venue_id=destination['id'],
                            start_lat=start_lat,
                            start_lng=start_lng,
                            end_lat=destination['latitude'],
                            end_lng=destination['longitude'])
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
                            venue_id=destination['id'],
                            start_lat=start_lat,
                            start_lng=start_lng,
                            end_lat=destination['latitude'],
                            end_lng=destination['longitude'])
        db.session.add(new_visit)
        db.session.commit()