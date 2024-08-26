from flask import Blueprint, session, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

scan_folder_bp = Blueprint('scan_folder', __name__)

FOLDER_ID = '1kfVpNTAvegKgiB2YyOTc0CGtMruywiuV'

@scan_folder_bp.route('/scan-folder', methods=['GET'])
def scan_folder():
    if 'credentials' not in session:
        return jsonify({"error": "User not authenticated"}), 401  # Return a JSON error response

    credentials = Credentials(**session['credentials'])
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        # Retrieve folder details
        folder_metadata = drive_service.files().get(
            fileId=FOLDER_ID,
            fields='name'
        ).execute()

        folder_name = folder_metadata.get('name', 'Unknown Folder')

        # List files in the specified folder
        results = drive_service.files().list(
            q=f"'{FOLDER_ID}' in parents",
            pageSize=10,
            fields="files(id, name, mimeType)"
        ).execute()

        files = results.get('files', [])

        # Log the number of files found
        logging.debug(f"Number of files found: {len(files)}")

        # Prepare a list of files to return
        file_list = [{'id': file['id'], 'name': file['name'], 'mimeType': file['mimeType']} for file in files]

        # Log each file found
        for file in file_list:
            logging.debug(f"File - ID: {file['id']}, Name: {file['name']}, Type: {file['mimeType']}")

        # Store folder name and file list in session
        session['folder_name'] = folder_name
        session['files'] = file_list

        # Return the list of files as JSON
        return {"folder_name": folder_name, "files": file_list}
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
