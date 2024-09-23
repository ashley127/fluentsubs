from flask import Blueprint, jsonify
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
    print("Attempting to download for processing...")
    try:
        drive_service = get_drive_service()

        # Directly download the file from Google Drive without using session
        request = drive_service.files().get_media(fileId=file_id)
        file_content = request.execute()

        # Determine file extension and create a file path
        file_ext = "mp4"  # Assuming it's an mp4 file for this example
        file_path = os.path.join("/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads", f"{file_id}.{file_ext}")

        # Save the file to the local file system
        with open(file_path, 'wb') as file:
            file.write(file_content)

        print(f"File {file_id} saved to {file_path}")
        return {"message": f"File downloaded successfully to {file_path}", "status_code": 200}

    except Exception as e:
        print(f"Failed to download file {file_id}: {e}")
        return {"error": f"Failed to download file: {e}", "status_code": 500}
