from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import session, flash
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """User of the app."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)

    @classmethod
    def user_logged_in(cls):
        if 'user_id' in session:
            return True
        return False

    @classmethod
    def log_user_out(cls):
        # remove user session and confirm user logout
        del session['user_id']
        flash('You are now logged out.')

    @classmethod
    def create_user(cls, email, password):

        # hash and salt user pw
        password = bcrypt.hashpw(password, bcrypt.gensalt())

        # create new user record and add to database
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.user_id

    @classmethod
    def log_user_in(cls, email, password):
        # retrieves user object from database
        user = User.query.filter_by(email=email).first()
        if user == None:
            flash('Uh-oh, we couldn\'t find you. Please register.')
            return False

        # logs current user out if session exists
        if 'user_id' in session:
            del session['user_id']

        # checks for password match and creates new session if successful
        if bcrypt.checkpw(password, user.password):
        # if user.password == password:
            session['user_id'] = user.user_id
            return True

        # redirects to login page if unsuccessful
        else:
            flash('Your password was incorrect. Please try again.')
            return False

    @classmethod
    def get_user_visit_history(cls):
        # retrieve all visit/venue data for logged in user and add to list
        visits = []
        raw_visits = Visit.query.filter(Visit.user_id==session['user_id']).order_by(Visit.visited_at).all()

        for visit in raw_visits:
            visits.append('%s, %s on %s' % (visit.venue.name, visit.venue.city, visit.visited_at.strftime('%B %d, %Y')))

        return visits

class Venue(db.Model):
    """Restaurant that a user has visited through the app."""

    __tablename__ = 'venues'

    venue_id = db.Column(db.String(75), primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    latitude = db.Column(db.Float(10,6), nullable=True)
    longitude = db.Column(db.Float(10,6), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    @classmethod
    def get_venue_img(cls):
        query_result = Visit.query.filter(Visit.user_id==session['user_id']).order_by('visited_at desc').first()
        image_url = query_result.venue.image
        return image_url


class Visit(db.Model):
    """Visit that a user has made to a venue."""

    __tablename__ = 'visits'

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    venue_id = db.Column(db.String, db.ForeignKey('venues.venue_id'),
                        nullable=False)
    ride_id = db.Column(db.String)
    uber_access_token = db.Column(db.String)
    visited_at = db.Column(db.DateTime,
                         default=datetime.utcnow)
    start_lat = db.Column(db.Float, nullable=False)
    start_lng = db.Column(db.Float, nullable=False)
    end_lat = db.Column(db.Float, nullable=False)
    end_lng = db.Column(db.Float, nullable=False)

    #Define relationship to user
    user = db.relationship('User',
                            backref=db.backref('visits', order_by=visit_id))

    #Define relationship to venue
    venue = db.relationship('Venue',
                            backref=db.backref('visits', order_by=visit_id))

    @classmethod
    def get_uber_ride_params(cls):
        destination = Visit.query.filter(Visit.user_id==session['user_id']).order_by('visited_at desc').first()
        coordinates = (destination.start_lat, destination.start_lng, destination.end_lat, destination.end_lng)
        city = destination.venue.city
        return coordinates, city

#############################################################
# Helper functions
def connect_to_db(app, db_uri="postgresql:///project"):
    """Connect the database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    Annie = User(user_id=1, email='annie@test.com', password='abc123')
    Analog = Venue(venue_id='analog-oakland', name='Analog', latitude=37.8040172, longitude=-122.2703549, city='Oakland', image='http://s3-media3.fl.yelpcdn.com/bphoto/NdTIPJGMzmxqpCdjXpeJcw/o.jpg')
    visit_1 = Visit(user_id=1, venue_id='analog-oakland', start_lat=37.7929816, start_lng=-122.4041434, end_lat=37.8040172, end_lng=-122.2703549)

    db.session.add_all([Annie, Analog, visit_1])
    db.session.commit()


if __name__ == "__main__":
    # If this file is run interactively, you will be able to interact directly
    # with the database
    from server import app
    connect_to_db(app)


    