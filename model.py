from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User of the app."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)


class Venue(db.Model):
    """Restaurant that a user has visited through the app."""

    __tablename__ = 'venues'

    venue_id = db.Column(db.String(75), primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    latitude = db.Column(db.Float(10,6), nullable=True)
    longitude = db.Column(db.Float(10,6), nullable=True)


class Visit(db.Model):
    """Visit that a user has made to a venue."""

    __tablename__ = 'visits'

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)
    venue_id = db.Column(db.String, db.ForeignKey('venues.venue_id'),
                        nullable=False)
    visited_at = db.Column(db.DateTime,
                         default=datetime.utcnow())
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
    Analog = Venue(venue_id='analog-oakland', name='Analog', latitude=37.8040172, longitude=-122.2703549)
    visit_1 = Visit(user_id=1, venue_id='analog-oakland', start_lat=37.7929816, start_lng=-122.4041434, end_lat=37.8040172, end_lng=-122.2703549)

    db.session.add_all([Annie, Analog, visit_1])
    db.session.commit()


if __name__ == "__main__":
    # If this file is run interactively, you will be able to interact directly
    # with the database
    from server import app
    connect_to_db(app)


    