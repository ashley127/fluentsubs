from flask import Blueprint, session, Response, redirect, url_for
from googleapiclient.discovery import build
from io import BytesIO
from google.oauth2.credentials import Credentials
import logging
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

                # Add the prefix "fluent-subs" to the original filename
                original_filename = file['name']
                tagged_filename = f"fluent-subs-{original_filename}"
                zip_file.writestr(tagged_filename, file_content)
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
