# TODO: Improve comments here

import os
import pdb
from flask import Flask, render_template, redirect, request, flash, session
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
import googlemaps

def get_start_coordinates(address):
    """Geocode and return user's current location."""

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