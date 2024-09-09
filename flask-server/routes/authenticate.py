from flask import Blueprint, session, redirect, url_for, flash
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os

auth_bp = Blueprint('auth', __name__)

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), '../fluent-subs-9ada8cd5d073.json')

@auth_bp.route('/login')
def login():
    try:
        # Authenticate using the service account
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])

        print("alive")

        # Create a Google Drive API service
        drive_service = build('drive', 'v3', credentials=credentials)

        # Store the credentials and some user information in the session
        session['credentials'] = credentials_to_dict(credentials)
        session['google_email'] = credentials.service_account_email  # Store the service account email
        session['google_name'] = 'Service Account'  # Just for display purposes

        return redirect(url_for('home'))
    except Exception as e:
        print(e)
        
        print("dead")
        flash(f"Error during login: {e}")
        return redirect(url_for('home'))

@auth_bp.route('/logout')
def logout():
    # Clear the session, effectively logging out the user
    session.clear()
    return redirect(url_for('home'))

def credentials_to_dict(credentials):
    """
    Converts the service account Credentials object to a dictionary format to store in session.
    """
    return {
        'token': credentials.token,
        'scopes': credentials.scopes,
        'service_account_email': credentials.service_account_email,
    }
