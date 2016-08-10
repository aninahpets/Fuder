# TODO: Improve comments here

import os
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
import googlemaps


def get_start_coordinates():
    gmaps = googlemaps.Client(key=os.environ['google_api_key'])
    geocode_result = gmaps.geocode('660 vernon st oakland ca')
    coordinates = geocode_result[0]['geometry']['location']
    start_latitude = coordinates['lat']
    start_longitude = coordinates['lng']
    return start_latitude, start_longitude


def request_ride(start_lat, start_lng, end_lat, end_lng):
    credentials = import_oauth2_credentials()
    # request app access from user
    uber_auth_flow = AuthorizationCodeGrant(
        uber_client_id,
        credentials.get('scopes'),
        uber_client_secret,
        'PLACEHOLDER_URI_FOR_CALLBACK',
        )

    # request access token from Uber
    uber_auth_url = uber_auth_flow.get_authorization_url()

    session = uber_auth_flow.get_session('/process_ride')
    uber_client = UberRidesClient(session, sandbox_mode=True)
    credentials = session.oauth2credential

    response = uber_client.request_ride(
        product_id = product_id,
        start_latitude = start_lat,
        start_longitude = start_lng,
        end_latitude = end_lat,
        end_longitude = end_lng
        )