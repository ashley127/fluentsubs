from flask import Blueprint, session, Response, redirect, url_for
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import logging

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
            return f"File not found in session.", 404

        request = drive_service.files().get_media(fileId=file_id)
        file_content = request.execute()

        # Preserve the original file extension
        file_ext = file_info['name'].split(".")[1]

        return Response(
            file_content,
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment;filename="{file_id}.{file_ext}"'
            }
        )
    except Exception as e:
        return f"Failed to download file: {e}", 500
