import os
import io
import pickle
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
storage_folder_path = './data/invoices'

def build_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

service = build_service()



def get_pdf_uris(folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    return {item['name']: item['id'] for item in items}

def download_pdf_from_google_drive(file_id, file_name, storage_folder_path:str='./data/invoices'):
    service = build_service()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    print(f"Downloaded {file_name}.")
    with open(os.path.join(storage_folder_path, file_name), 'wb') as f:
        f.write(fh.getvalue())

def download_all_pdf_files_from_folder(folder_id, service):
    uris = get_pdf_uris(service, folder_id)
    for file_name, file_id in uris.items():
        download_pdf_from_google_drive(file_id, file_name)

if __name__ == '__main__':
    folder_id = 'xyz'
    service = build_service()
