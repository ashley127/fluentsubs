from flask import Blueprint, session, Response, redirect, url_for, jsonify
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import logging
import os
from io import BytesIO
import zipfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)

download_all_bp = Blueprint('download_all', __name__)

@download_all_bp.route('/download-all')
def download_all():
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))

    credentials = Credentials(**session['credentials'])
    drive_service = build('drive', 'v3', credentials=credentials)

    files = session.get('files', [])
    if not files:
        return redirect(url_for('home'))

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files:
            try:
                request = drive_service.files().get_media(fileId=file['id'])
                file_content = request.execute()

                # Use file_id with the original file extension for naming
                file_id = file['id']
                zip_file.writestr(f"{file_id}", file_content)
            except Exception as e:
                logging.error(f"Failed to download file {file['name']}: {e}")

    zip_buffer.seek(0)

    return Response(
        zip_buffer.getvalue(),
        mimetype='application/zip',
        headers={
            'Content-Disposition': 'attachment;filename=fluent-subs-files.zip'
        }
    )

@download_all_bp.route('/download-file/<file_id>')
def download_file(file_id):
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))

    credentials = Credentials(**session['credentials'])
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        files = session.get('files', [])
        file_info = next((file for file in files if file['id'] == file_id), None)
        if not file_info:
            return jsonify({"error": "File not found in session."}), 404

        request = drive_service.files().get_media(fileId=file_id)
        file_content = request.execute()

        # Determine file extension and create a file path
        file_name = file_info['name']
        file_ext = file_name.split(".")[-1] if "." in file_name else "bin"
        file_path = os.path.join("/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads", f"{file_id}.{file_ext}")

        # Save the file to the local file system
        with open(file_path, 'wb') as file:
            file.write(file_content)

        logging.info(f"File {file_id} saved to {file_path}")

        # Return success message or the file path
        return {"message": f"File downloaded successfully to {file_path}", "status_code": 200}

    except Exception as e:
        logging.error(f"Failed to download file {file_id}: {e}")
        return jsonify({"error": f"Failed to download file: {e}"}), 500