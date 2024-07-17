from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)
    token_uri = db.Column(db.String, nullable=False)
    client_id = db.Column(db.String, nullable=False)
    client_secret = db.Column(db.String, nullable=False)
    scopes = db.Column(db.String, nullable=False)
