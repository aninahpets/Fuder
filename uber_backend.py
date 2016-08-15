# TODO: Improve comments here

import os
import pdb
from flask import Flask, render_template, redirect, request, flash, session
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
import googlemaps


def get_start_coordinates():
    user_location = request.args.get('user-address')
    gmaps = googlemaps.Client(key=os.environ['google_api_key'])
    geocode_result = gmaps.geocode('%s' % user_location)
    coordinates = geocode_result[0]['geometry']['location']
    start_latitude = coordinates['lat']
    start_longitude = coordinates['lng']
 
    return start_latitude, start_longitude


def request_ride(start_lat, start_lng, end_lat, end_lng):

    uber_auth_flow = AuthorizationCodeGrant(
        os.environ['uber_client_id'],
        ['request'],
        os.environ['uber_client_secret'],
        'http://localhost:5000/callback',
        )

    uber_auth_url = uber_auth_flow.get_authorization_url()
    return uber_auth_url
    # send user to URL uber_auth_url to authorize app access

    session = uber_auth_flow.get_session('http://0.0.0.0:5000/callback')
    uber_client = UberRidesClient(session, sandbox_mode=True)
    credentials = session.oauth2credential

    response = uber_client.request_ride(
        start_latitude = start_lat,
        start_longitude = start_lng,
        end_latitude = end_lat,
        end_longitude = end_lng
        )

    ride_details = response.json
    ride_id = ride_details.get('request_id')