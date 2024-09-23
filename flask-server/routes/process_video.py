from flask import Blueprint, request, jsonify
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import os

from routes.download_all import download_file
from routes.transcribe import transcribe_file
from routes.subtitle import create_video

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
        
        print(f"Processing file IDs (from request): {file_ids}")

        for file_id in file_ids:
            try:
                print(f"processing file: {file_id}")

                print(f"attempting to download file: {file_id}")
                download_response = download_file(file_id)
                if download_response["status_code"] != 200:
                    print(f'download failed: {download_response}')
                    return jsonify({"error": f"Failed to download file {file_id}, due to {download_response}"}), 500

                print(f"attempting to transcribe file: {file_id}")
                transcribe_response = transcribe_file(file_id)
                if transcribe_response["status_code"] != 200:
                    print(f'transcribe failed: {transcribe_response}')
                    return jsonify({"error": f"Failed to transcribe file {file_id}, due to {transcribe_response}"}), 500
                
                print(f"attempting to add subtitles and create final video: {file_id}")
                subtitle_response = create_video(file_id)
                if subtitle_response["status_code"] != 200:
                    print(f'subtitle failed: {subtitle_response}')
                    return jsonify({"error": f"Failed to subtitle file {file_id}, due to {subtitle_response}"}), 500

            except Exception as e:
                print(f"Error while processing file {file_id}: {e}")
                return jsonify({"error": f"Error processing file {file_id}: {e}"}), 500

        return jsonify({"message": "Files processed successfully", "status_code": 200})

    except Exception as e:
        print(f"Error while processing video: {e}")
        return jsonify({"error": f"Error while processing video: {e}"}), 500
