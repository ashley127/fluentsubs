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

from routes.scan_folder import scan_blueprint
app.register_blueprint(scan_blueprint)

from routes.download_all import download_all_bp
app.register_blueprint(download_all_bp)

from routes.transcribe import transcribe_bp
app.register_blueprint(transcribe_bp)

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
            <p><a href="/scan-folder"><button>Scan Google Drive Files</button></a></p>
            <p><a href="/logout"><button>Logout</button></a></p>
            
            <h2>Scanned Folder</h2>
            <p>Folder Name: {folder_name}</p>
            <ul>
                {''.join(f'''
                    <li>
                        {file["name"]} (ID: {file["id"]}, Type: {file["mimeType"]})
                        <p>
                            <a href="/download-file/{file["id"]}"><button>Download</button></a>
                            <form action="/transcribe-file/{file["id"]}" method="post" style="display:inline;" onsubmit="showSpinner(this);">
                                <button type="submit">Transcribe</button>
                                <span class="spinner" style="display:none;">⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏</span>
                            </form>
                        </p>
                        <p>{transcriptions.get(file["id"], "No transcription available")}</p>
                    </li>''' for file in files)}
            </ul>

            <p><a href="/download-all"><button>Download All Files</button></a></p>

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
        # If not authenticated, prompt to log in
        return 'Welcome to the Home Page! <a href="/login">Login with Google</a>'

if __name__ == '__main__':
    app.run(debug=True)
