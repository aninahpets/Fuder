#Fuder

Fuder is an application using the Yelp and Uber APIs (as well as the Google Places API for autocomplete and geocoding) to simplify and add an element of excitement to user excursions. Users authorize the app to make Uber ride requests on their behalf and provide any venue or pricing preferences they may have, along with their current location (the only required input). Fuder does the rest of the work, using the user’s inputs to retrieve a corresponding highly-rated Yelp business in the vicinity, and making an Uber ride request to transport the user from their current location to the mystery destination. Fuder also tracks users’ visit history and makes this accessible.

##Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)

## <a name="technologies"></a>Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: Yelp, Uber, Google Places<br/>

## <a name="features"></a>Features

## <a name="install"></a>Installation

To run Fuder, please clone or fork this repo:

```
https://github.com/aninahpets/Fuder.git
```

Install PostgreSQL (Mac OSX)

Create and activate a virtual environment inside your Fuder directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [Yelp API](https://www.yelp.com/developers/v3/preview), the [Uber API](https://developer.uber.com/docs/rides/getting-started), and the [Google Places API](https://developers.google.com/places/).

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export yelp_app_id="YOURKEYHERE"
export yelp_app_secret="YOURKEYHERE"
export uber_client_id="YOURKEYHERE"
export uber_client_secret="YOURKEYHERE"
export uber_server_token="YOURKEYHERE"
export google_api_key="YOURKEYHERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
python -i model.py
db.create_all()
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access Fuder.