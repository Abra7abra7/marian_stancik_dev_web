import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

KEY_PATH = r"C:\Users\mstancik\.gemini\credentials\hermes-crm-key.json"
SPREADSHEET_ID = "1mcVQxHMu1SavnoJussw9KCpleT-qhFs8FJMe4F8h5PM"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

try:
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    sheets_service = build("sheets", "v4", credentials=creds)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    test_row = [[now, "Marian Stančík (Live Test)", "marian@marianstancik.dev", "AI GEO Audit", "€199", "https://marianstancik.dev", "Testovacie prepojenie: Agent -> Google Sheets MCP!", "Web Lead Form", "Aktívny"]]

    result = sheets_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",
        valueInputOption="USER_ENTERED",
        body={"values": test_row}
    ).execute()
    print("SUCCESS: Live test lead appended successfully to your Google Sheet!")
    print("Updated range:", result.get("updates", {}).get("updatedRange"))

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
