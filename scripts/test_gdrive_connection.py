import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_PATH = r"C:\Users\mstancik\.gemini\credentials\hermes-crm-key.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

try:
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    results = drive_service.files().list(pageSize=10, fields="files(id, name, mimeType)").execute()
    files = results.get("files", [])
    print(f"SUCCESS: Connected to Google Drive as {creds.service_account_email}!")
    print(f"Total shared files visible to agent: {len(files)}")
    for f in files:
        print(f" - {f['name']} ({f['mimeType']}) [ID: {f['id']}]")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
