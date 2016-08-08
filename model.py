from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.model):
    """User of the app."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    password = db.Column(db.String(75), nullable=False)


class Venue(db.model):
    """Restaurants that app has sent users to."""

    __tablename__ = 'venues'

    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Decimal(10,6), nullable=False)
    longitude = db.Column(db.Decimal(10,6), nullable=False)


class Visit(db.model):
    """Visits users have made to venues."""

    __tablename__ = 'visits'

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
        nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(venues.venue_id),
        nullable=False)
    visited_at = db.Column(db.Integer, db.DateTime,
        default=datetime.datetime.utcnow)

    #Define relationship to user
    user = db.relationship('User', backref=db.backref('visits',
        order_by=visit_id))

    #Define relationship to venue
    venue = db.relationship('Venue', backref=db.backref('visits',
        order_by=visit_id))



#############################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to the Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurantrides'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # If this file is run interactively, you will be able to interact directly
    # with the database
    from server import app
    connect_to_db(app)