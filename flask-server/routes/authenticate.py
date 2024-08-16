from flask import Blueprint, redirect, url_for, session, request
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow
import os
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

auth_bp = Blueprint('auth', __name__)

SCOPES = ["https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/userinfo.profile",
          "https://www.googleapis.com/auth/userinfo.email",
          "openid"]
REDIRECT_URI = os.getenv('REDIRECT_URI', "http://127.0.0.1:5000/oauth2callback")

# Load credentials from the JSON file
credentials_path = os.path.join(os.path.dirname(__file__), '../client_secret.json')
print(credentials_path)
with open(credentials_path) as f:
    credentials_data = json.load(f)

flow = Flow.from_client_config(
    credentials_data,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@auth_bp.route("/login")
def login():
    authorization_url, state = flow.authorization_url(access_type='offline')
    session["state"] = state
    return redirect(authorization_url)

@auth_bp.route("/oauth2callback")
def oauth2callback():
    try:
        flow.fetch_token(authorization_response=request.url)

        # Check and log state values
        if "state" not in session or session["state"] != request.args.get("state"):
            return "State does not match!", 500

        credentials = flow.credentials

        # Log credentials and id_token
        if not credentials:
            return "No credentials obtained.", 500
        if not credentials.id_token:
            return "No ID token obtained.", 500

        request_session = google_requests.Request()

        id_info = id_token.verify_oauth2_token(
            credentials.id_token, request_session, credentials_data['web']['client_id']
        )

        # Log ID info
        if not id_info:
            return "ID token verification failed.", 500

        session["google_id"] = id_info.get("sub")
        session["google_name"] = id_info.get("name")
        session["google_email"] = id_info.get("email")

        return redirect(url_for("home"))
    except Exception as e:
        # Log the exception details
        return f"An error occurred during the callback: {e}", 500


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
