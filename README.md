#Fuder

Fuder is an application using the Yelp and Uber APIs (as well as the Google Places API for autocomplete and geocoding) to simplify and add an element of excitement to user excursions. Users authorize the app to make Uber ride requests on their behalf and provide any venue or pricing preferences they may have, along with their current location (the only required user input). Fuder does the rest of the work, retrieving a corresponding highly-rated Yelp business in the vicinity, and making an Uber ride request to transport the user from their current location to the mystery destination. Fuder also tracks users’ visit history and makes this accessible.

##Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)

## <a name="technologies"></a>Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: Yelp (v3), Uber, Google Places<br/>

## <a name="features"></a>Features

Using a simple UI, users can choose to either be taken to a bar or restaurant:
![](https://cloud.githubusercontent.com/assets/18404713/18288887/059969d2-7432-11e6-9957-9dc41d04d753.png)

Users can then select their pricing and venue preferences:
![](https://cloud.githubusercontent.com/assets/18404713/18288891/05ac5092-7432-11e6-9efa-73d7d0ca365c.png)

They then enter their location:
![](https://cloud.githubusercontent.com/assets/18404713/18288890/05ab00ca-7432-11e6-82b9-e999ce98efc3.png)

Uber prompts them for authorization:
![](https://cloud.githubusercontent.com/assets/18404713/18288892/05afdb68-7432-11e6-8934-3874fad5d45d.png)
![](https://cloud.githubusercontent.com/assets/18404713/18288884/05973676-7432-11e6-8871-9d11484a7446.png)

The request is then completed and users can view a "sneak preview" while they wait for their ride:
![](https://cloud.githubusercontent.com/assets/18404713/18288885/0597a5e8-7432-11e6-96fb-f5743f78792f.png)
![](https://cloud.githubusercontent.com/assets/18404713/18288889/059a2958-7432-11e6-8abd-0892678ecac5.png)

Users can also view their visit history:
![](https://cloud.githubusercontent.com/assets/18404713/18288886/05989da4-7432-11e6-98c7-4a2be7105e92.png)

The app also has a user management system incorporating password encryption.

## <a name="install"></a>Installation

To run Fuder:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/aninahpets/Fuder.git
```

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