from flask import Flask, redirect, request, url_for, session
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

bp = Blueprint('main', __name__)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        save_file_to_drive(file, session['credentials'])
        return 'File uploaded successfully!'
    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    '''
