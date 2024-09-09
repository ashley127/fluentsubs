from flask import Blueprint, request, jsonify, session
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import os

process_video_bp = Blueprint('process_video', __name__)

SERVICE_ACCOUNT_FILE = 'fluent-subs-9ada8cd5d073.json'

def get_drive_service():
    credentials = ServiceAccountCredentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=credentials)

@process_video_bp.route('/process-video', methods=['POST'])
def process_video():
    global request
    print("Processing video...")

    try:
        # Check the content type and log it
        print(request)
        print(f"Content-Type: {request.content_type}")
        
        # Attempt to get JSON data from the request
        data = request.json
        if data is None:
            print("No JSON data found in the request.")
            return jsonify({"error": "No JSON data found in the request."}), 400
        
        print(f"Request JSON: {data}")
        
        file_ids = data.get('file_ids', [])
        if not file_ids:
            print("No file IDs provided.")
            return jsonify({"error": "No file IDs provided."}), 400
        
        print(f"Processing file IDs: {file_ids}")

        # Debug print to check the session data
        files_in_session = session.get('files', [])
        print(f"Files in session: {files_in_session}")

        for file_id in file_ids:
            file_info = next((file for file in files_in_session if file['id'] == file_id), None)
            
            if not file_info:
                print(f"File with ID {file_id} not found in session.")
                continue
            
            drive_service = get_drive_service()
            request = drive_service.files().get_media(fileId=file_id)
            file_content = request.execute()

            file_name = file_info['name']
            file_ext = file_name.split(".")[-1] if "." in file_name else "bin"
            file_path = os.path.join("/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads", f"{file_id}.{file_ext}")

            with open(file_path, 'wb') as file:
                file.write(file_content)

            print(f"File {file_id} saved to {file_path}")

        return jsonify({"message": "Files processed successfully", "status_code": 200})

    except Exception as e:
        print(f"Error while processing video: {e}")
        return jsonify({"error": f"Error while processing video: {e}"}), 500
