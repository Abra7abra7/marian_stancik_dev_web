"""
Marian Stancik — Google Drive & Sheets MCP Server
Provides autonomous agent tools for managing Google Drive files, client folders, and CRM Google Sheets.
"""
import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from mcp.server.fastmcp import FastMCP

KEY_PATH = os.environ.get("GDRIVE_KEY_PATH", r"C:\Users\mstancik\.gemini\credentials\hermes-crm-key.json")
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

mcp = FastMCP("hermes-gdrive-mcp")

def get_services():
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    sheets_service = build("sheets", "v4", credentials=creds)
    return drive_service, sheets_service

@mcp.tool()
def list_drive_files(page_size: int = 20) -> list:
    """Lists files and folders accessible by the agent on Google Drive."""
    drive, _ = get_services()
    results = drive.files().list(
        pageSize=page_size,
        fields="files(id, name, mimeType, webViewLink, createdTime)"
    ).execute()
    return results.get("files", [])

@mcp.tool()
def create_client_folder(name: str, parent_folder_id: str = "") -> dict:
    """Creates a dedicated client directory on Google Drive."""
    drive, _ = get_services()
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_folder_id:
        meta["parents"] = [parent_folder_id]
    folder = drive.files().create(body=meta, fields="id, name, webViewLink").execute()
    return {"status": "created", "folder_id": folder["id"], "name": folder["name"], "link": folder.get("webViewLink", "")}

@mcp.tool()
def append_lead_to_sheet(sheet_id: str, email: str, name: str = "", product: str = "", price: str = "", message: str = "", source: str = "web") -> dict:
    """Appends a new customer lead or audit order to a Google Spreadsheet."""
    _, sheets = get_services()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row_values = [[now, name, email, product, price, message, source, "New"]]
    body = {"values": row_values}
    result = sheets.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range="A1",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    return {"status": "appended", "updated_range": result.get("updates", {}).get("updatedRange", "")}

@mcp.tool()
def upload_file_to_drive(file_path: str, folder_id: str = "") -> dict:
    """Uploads a local file (e.g. PDF audit, report) to Google Drive."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    drive, _ = get_services()
    file_name = os.path.basename(file_path)
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    uploaded = drive.files().create(body=file_metadata, media_body=media, fields="id, name, webViewLink").execute()
    return {"status": "uploaded", "file_id": uploaded["id"], "name": uploaded["name"], "link": uploaded.get("webViewLink", "")}

if __name__ == "__main__":
    mcp.run()
