from flask import request, jsonify, Blueprint, session
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import os
from flask_session import Session

upload_bp = Blueprint('upload', __name__)

# Load service account credentials from the JSON file
credentials_path = os.path.join(os.path.dirname(__file__), '../fluent-subs-9ada8cd5d073.json')
SCOPES = ["https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_file(
    credentials_path, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    print("Upload starting...")

    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        temp_file_path = os.path.join('/tmp', file.filename)
        file.save(temp_file_path)
        print(f"File saved to {temp_file_path}")

        folder_id = "1kfVpNTAvegKgiB2YyOTc0CGtMruywiuV"  # Replace with your shared folder ID
        file_metadata = {
            'name': file.filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(temp_file_path, mimetype=file.content_type)
        drive_file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        print(f"File uploaded to Google Drive with ID: {drive_file.get('id')}")

        os.remove(temp_file_path)
        print(f"Temporary file removed: {temp_file_path}")

        # Store file information in session
        files = session.get('files', [])
        files.append({
            'id': drive_file.get('id'),
            'name': file.filename
        })
        session['files'] = files

        return jsonify({"message": "File uploaded successfully", "file_id": drive_file.get('id')})

    except Exception as e:
        print(f"Error during file upload: {str(e)}")
        return jsonify({"error": str(e)}), 500
