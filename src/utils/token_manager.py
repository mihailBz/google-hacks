from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from database.models import UserCredentials, db


def get_credentials(user_id):
    user_creds = UserCredentials.query.filter_by(user_id=user_id).first()
    if not user_creds:
        return None

    creds = Credentials(
        token=user_creds.token,
        refresh_token=user_creds.refresh_token,
        token_uri=user_creds.token_uri,
        client_id=user_creds.client_id,
        client_secret=user_creds.client_secret,
        scopes=user_creds.scopes,
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        user_creds.token = creds.token
        db.session.commit()
    return creds
