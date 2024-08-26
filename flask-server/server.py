from flask import Flask, session, url_for, redirect, render_template_string, request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.getenv('GOOGLE_CLIENT_SECRET')

# Register blueprints
from routes.authenticate import auth_bp
app.register_blueprint(auth_bp)

from routes.scan_folder import scan_folder_bp
app.register_blueprint(scan_folder_bp)

from routes.download_all import download_all_bp
app.register_blueprint(download_all_bp)

from routes.transcribe import transcribe_bp
app.register_blueprint(transcribe_bp)

from routes.subtitle import subtitle_bp
app.register_blueprint(subtitle_bp)

from routes.process_video import process_video_bp
app.register_blueprint(process_video_bp)

@app.route('/')
def home():
    # Check if the user is authenticated
    if 'google_email' in session:
        # If authenticated, show a button to scan files
        folder_name = session.get('folder_name', 'No folder scanned yet')
        files = session.get('files', [])
        transcriptions = session.get('transcriptions', {})

        # Define a simple HTML template directly in the route
        html_content = f'''
            <h1>Welcome, {session['google_name']}</h1>
            <p><a href="{url_for('scan_folder.scan_folder')}"><button>Scan Google Drive Files</button></a></p>
            <p><a href="{url_for('auth.logout')}"><button>Logout</button></a></p>
            
            <h2>Scanned Folder</h2>
            <p>Folder Name: {folder_name}</p>
            <ul>
                {''.join(f'''
                    <li>
                        {file["name"]} (ID: {file["id"]}, Type: {file["mimeType"]})
                        <p>
                            <a href="{url_for('download_all.download_file', file_id=file['id'])}"><button>Download</button></a>
                            <form action="{url_for('transcribe.transcribe_file', file_id=file['id'])}" method="post" style="display:inline;" onsubmit="showSpinner(this);">
                                <button type="submit">Transcribe</button>
                                <span class="spinner" style="display:none;">⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏</span>
                            </form>
                            {f'''
                                <form action="{url_for('subtitle.create_video', file_id=file['id'])}" method="post" style="display:inline;" onsubmit="showSpinner(this);">
                                    <button type="submit">Add Subtitles</button>
                                    <span class="spinner" style="display:none;">⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏</span>
                                </form>
                                <a href="{url_for('process_video.download_video', file_id=file['id'])}"><button>Download Final Video</button></a>
                            ''' if file["id"] in transcriptions else ''}
                        </p>
                        <p>{transcriptions.get(file["id"], "No transcription available")}</p>
                    </li>''' for file in files)}
            </ul>

            <p><a href="{url_for('download_all.download_all')}"><button>Download All Files</button></a></p>

            <p><form action="{url_for('process_video.process_video')}" method="post" onsubmit="showSpinner(this);">
                <button type="submit">Process All Files</button>
                <span class="spinner" style="display:none;">⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏</span>
            </form></p>

            <script>
                function showSpinner(form) {{
                    const spinner = form.querySelector('.spinner');
                    spinner.style.display = 'inline';
                    let frame = 0;
                    const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
                    setInterval(() => {{
                        spinner.textContent = frames[frame % frames.length];
                        frame++;
                    }}, 100);
                }}
            </script>
        '''

        return render_template_string(html_content)
    else:
        return f'Welcome to the Home Page! <a href="{url_for('auth.login')}">Login with Google</a>'



if __name__ == '__main__':
    app.run(debug=True)
