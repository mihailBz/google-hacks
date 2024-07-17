import json

from flask import (
    Flask,
    jsonify,
    redirect,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from config import Config
from database.models import UserCredentials, db
from utils.token_manager import get_credentials

# todo refactor this
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    # "email",
    # "profile",
    "https://www.googleapis.com/auth/calendar",
]

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

with open(app.config["GOOGLE_CLIENT_SECRETS_FILE"]) as f:
    client_secrets = json.load(f)


@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        app.config["GOOGLE_CLIENT_SECRETS_FILE"], scopes=SCOPES
    )
    flow.redirect_uri = url_for("oauth2callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]
    flow = Flow.from_client_secrets_file(
        app.config["GOOGLE_CLIENT_SECRETS_FILE"], scopes=SCOPES, state=state
    )
    flow.redirect_uri = url_for("oauth2callback", _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    user_info = get_user_info(credentials)
    user_id = user_info["id"]
    email = user_info["email"]

    user_creds = UserCredentials.query.filter_by(user_id=user_id).first()
    if user_creds:
        user_creds.token = credentials.token
        user_creds.refresh_token = credentials.refresh_token
        user_creds.token_uri = credentials.token_uri
        user_creds.client_id = credentials.client_id
        user_creds.client_secret = credentials.client_secret
        user_creds.scopes = " ".join(credentials.scopes)
    else:
        user_creds = UserCredentials(
            user_id=user_id,
            email=email,
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=" ".join(credentials.scopes),
        )
        db.session.add(user_creds)
    db.session.commit()

    access_token = create_access_token(identity=user_id)
    return redirect(url_for("serve_index", access_token=access_token))


def get_user_info(credentials):
    if not credentials or not credentials.valid:
        raise Exception("Invalid credentials")
    user_info_service = build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    return user_info


@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/api/read-calendar", methods=["GET"])
@jwt_required()
def test_read_calendar():
    user_id = get_jwt_identity()
    creds = get_credentials(user_id)
    if not creds:
        return redirect(url_for("authorize"))

    calendar_service = build("calendar", "v3", credentials=creds)
    events = calendar_service.events().list(calendarId="primary").execute()
    return jsonify(events), 200


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)
