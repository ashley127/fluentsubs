from flask import Blueprint, jsonify, session, redirect, url_for, send_file
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import os

download_all_bp = Blueprint('download_all', __name__)

SERVICE_ACCOUNT_FILE = 'fluent-subs-9ada8cd5d073.json'

# Function to build the drive service using a service account
def get_drive_service():
    credentials = ServiceAccountCredentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=credentials)
@download_all_bp.route('/download-file/<file_id>')
def download_file(file_id):
    try:
        drive_service = get_drive_service()

        # Retrieve files from the session and print their IDs
        files = session.get('files', [])
        file_ids = [file['id'] for file in files]  # Extract file IDs from the session
        print(f"File IDs in session: {file_ids}")  # Print the file IDs for debugging

        # Find the specific file by file_id
        file_info = next((file for file in files if file['id'] == file_id), None)
        if not file_info:
            print(f"File with ID {file_id} not found in session.")  # Additional debug statement
            return {"error": "File not found in session.", "status_code": 404}

        # Download the file from Google Drive
        request = drive_service.files().get_media(fileId=file_id)
        file_content = request.execute()

        # Determine file extension and create a file path
        file_name = file_info['name']
        file_ext = file_name.split(".")[-1] if "." in file_name else "bin"
        file_path = os.path.join("/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads", f"{file_id}.{file_ext}")

        # Save the file to the local file system
        with open(file_path, 'wb') as file:
            file.write(file_content)

        print(f"File {file_id} saved to {file_path}")
        return {"message": f"File downloaded successfully to {file_path}", "status_code": 200}

    except Exception as e:
        print(f"Failed to download file {file_id}: {e}")
        return jsonify({"error": f"Failed to download file: {e}"}), 500
