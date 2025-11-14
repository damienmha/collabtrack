from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object *without* the app yet.
# It will be initialized with the app in app.py.
db = SQLAlchemy()