from flask import Blueprint, jsonify, session, send_file, request
import os
from routes.scan_folder import scan_folder
from routes.download_all import download_file
from routes.transcribe import transcribe_file
from routes.subtitle import create_video

process_video_bp = Blueprint('process_video', __name__)

scanned_files = set()

@process_video_bp.route('/process-video', methods=['POST'])
def process_video():
    try:
        print("starting process")

        result = scan_folder()
        print("scanning results: ", result)
        
        if 'error' in result:
            return jsonify({"error": "Failed to scan folder"}), 500
        
        print("no error in scanning")

        new_files = result['files']

        print("new files found", new_files)
        for file_info in new_files:

            print("processing file:", file_info)

            file_id = file_info['id']

            if file_id in scanned_files:
                continue

            scanned_files.add(file_id)

            print("attempting download")
            download_response = download_file(file_id)
            if download_response["status_code"] != 200:
                return jsonify({"error": f"Failed to download file {file_id}"}), 500

            print("attempting to transcribe file")
            transcribe_response = transcribe_file(file_id)
            if transcribe_response["status_code"] != 200:
                return jsonify({"error": f"Transcription failed for file {file_id}"}), 500

            print("attempting to create final video")
            subtitle_response = create_video(file_id)
            if subtitle_response["status_code"] != 200:
                return jsonify({"error": f"Subtitle creation failed for file {file_id}"}), 500

            print("attempting to serve final video")
            final_video_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}_with_subtitles.mp4'
            if not os.path.exists(final_video_path):
                return jsonify({"error": f"Final video file not found for {file_id}"}), 404
            
            return send_file(final_video_path, as_attachment=True)

        return jsonify({"message": "Processing complete, but no new files were found."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@process_video_bp.route('/download-video/<file_id>', methods=['GET'])
def download_video(file_id):
    try:
        final_video_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}_with_subtitles.mp4'
        if not os.path.exists(final_video_path):
            return jsonify({"error": "Final video file not found."}), 404

        return send_file(final_video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
