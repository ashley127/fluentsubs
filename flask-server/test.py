import os
import pickle
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Path to your client_secret.json file
CLIENT_SECRET_FILE = 'client_secret.json'

# Define the scope you need
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Authenticate and create a Google Drive API service."""
    creds = None
    # Token file stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(service, folder_id):
    """List files in the specified Google Drive folder."""
    try:
        # List files in the specified folder
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=10,
            fields="files(id, name, mimeType)"
        ).execute()

        files = results.get('files', [])

        # Log the number of files found
        logging.debug(f"Number of files found: {len(files)}")

        if not files:
            logging.debug("No files found in the folder.")
            return "No files found in the folder."

        # Prepare a list of files to display
        file_list = [{'id': file['id'], 'name': file['name'], 'mimeType': file['mimeType']} for file in files]

        # Log each file found
        for file in file_list:
            logging.debug(f"File - ID: {file['id']}, Name: {file['name']}, Type: {file['mimeType']}")

        return file_list

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

if __name__ == "__main__":
    service = authenticate()
    folder_id = 'your-folder-id'  # Replace with your folder ID
    files = list_files_in_folder(service, folder_id)
    print(files)
