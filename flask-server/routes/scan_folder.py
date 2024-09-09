from flask import Blueprint, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

scan_folder_bp = Blueprint('scan_folder', __name__)

FOLDER_ID = '1kfVpNTAvegKgiB2YyOTc0CGtMruywiuV'

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'fluent-subs-9ada8cd5d073.json'

def scan_folder():
    try:
        # Load the service account credentials
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/drive']
        )

        drive_service = build('drive', 'v3', credentials=credentials)

        # Retrieve folder details
        folder_metadata = drive_service.files().get(
            fileId=FOLDER_ID,
            fields='name'
        ).execute()
        folder_name = folder_metadata.get('name', 'Unknown Folder')
        print(f"Folder name retrieved: {folder_name}")

        # List files in the specified folder
        results = drive_service.files().list(
            q=f"'{FOLDER_ID}' in parents",
            pageSize=10,
            fields="files(id, name, mimeType)"
        ).execute()
        files = results.get('files', [])
        print(f"Number of files found: {len(files)}")

        # Prepare a list of files to return
        file_list = [{'id': file['id'], 'name': file['name'], 'mimeType': file['mimeType']} for file in files]

        for file in file_list:
            print(f"File - ID: {file['id']}, Name: {file['name']}, Type: {file['mimeType']}")

        # Return the list of files as JSON
        return jsonify({"folder_name": folder_name, "files": file_list})

    except Exception as e:
        print(f"An error occurred during folder scan: {e}")
        return jsonify({"error": str(e)}), 500
