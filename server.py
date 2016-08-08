from flask import (Flask, render_template, redirect, request, session)
from model import User, Venue, Visit, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    """Homepage"""

    return render_template('index.html')

@app.route('/request')
    """User view while Uber ride request is processing"""

    return render_template('processing.html')


@app.route('/history')
    """User view of their complete venue visit history"""

    return render_template('visit-history.html')