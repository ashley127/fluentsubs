from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.getenv('GOOGLE_CLIENT_SECRET')

# Register blueprints and define routes
from routes.authenticate import auth_bp
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return 'Welcome to the Home Page! <a href="/login">Login with Google</a>'

if __name__ == '__main__':
    app.run(debug=True)
