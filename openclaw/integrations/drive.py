"""Google Drive integration - Simplified access to files and folders"""

import logging
import os
import pickle
from typing import Dict, List, Optional, BinaryIO
from io import BytesIO

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


class DriveIntegration:
    """
    Simplified Google Drive integration.

    Easy access to:
    - List files and folders
    - Search files
    - Download files
    - Upload files (if write scope enabled)
    - Get file metadata
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
    ):
        """
        Initialize Google Drive integration.

        Args:
            credentials_path: Path to OAuth credentials JSON
            token_path: Path to save/load token
        """
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_OAUTH_CREDENTIALS_FILE", "google_oauth_credentials.json"
        )
        self.token_path = token_path or os.getenv(
            "GOOGLE_TOKEN_FILE", "google_token.pickle"
        )
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None

        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    logger.warning(
                        f"Credentials file not found: {self.credentials_path}"
                    )
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("drive", "v3", credentials=creds)
        logger.info("Google Drive API authenticated successfully")

    async def list_files(
        self,
        query: Optional[str] = None,
        max_results: int = 100,
        folder_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        List files in Google Drive.

        Args:
            query: Custom query (e.g., "name contains 'project'")
            max_results: Maximum number of files to return
            folder_id: List files in specific folder

        Returns:
            List of file dictionaries with id, name, mimeType, etc.
        """
        if not self.service:
            logger.error("Drive service not initialized")
            return []

        try:
            # Build query
            queries = []
            if query:
                queries.append(query)
            if folder_id:
                queries.append(f"'{folder_id}' in parents")

            final_query = " and ".join(queries) if queries else None

            results = (
                self.service.files()
                .list(
                    q=final_query,
                    pageSize=max_results,
                    fields="files(id, name, mimeType, size, modifiedTime, webViewLink)",
                )
                .execute()
            )

            return results.get("files", [])

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []

    async def search_files(
        self, name: Optional[str] = None, file_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for files by name or type.

        Args:
            name: Search for files containing this name
            file_type: MIME type (e.g., 'application/pdf', 'image/jpeg')

        Returns:
            List of matching files
        """
        queries = []

        if name:
            queries.append(f"name contains '{name}'")
        if file_type:
            queries.append(f"mimeType='{file_type}'")

        query = " and ".join(queries) if queries else None
        return await self.list_files(query=query)

    async def get_file_metadata(self, file_id: str) -> Optional[Dict]:
        """Get detailed metadata for a file"""
        if not self.service:
            return None

        try:
            file = (
                self.service.files()
                .get(
                    fileId=file_id,
                    fields="id, name, mimeType, size, modifiedTime, webViewLink, owners",
                )
                .execute()
            )
            return file
        except Exception as e:
            logger.error(f"Error getting file metadata: {e}")
            return None

    async def download_file(self, file_id: str, output_path: Optional[str] = None) -> Optional[bytes]:
        """
        Download a file from Google Drive.

        Args:
            file_id: ID of the file to download
            output_path: Optional path to save file (if None, returns bytes)

        Returns:
            File bytes if output_path is None, otherwise None
        """
        if not self.service:
            return None

        try:
            request = self.service.files().get_media(fileId=file_id)

            if output_path:
                # Download to file
                with open(output_path, 'wb') as f:
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                logger.info(f"Downloaded file to {output_path}")
                return None
            else:
                # Download to memory
                fh = BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                return fh.getvalue()

        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return None

    async def get_recent_files(self, max_results: int = 20) -> List[Dict]:
        """Get recently modified files"""
        return await self.list_files(
            query="trashed=false",
            max_results=max_results,
        )

    async def search_documents(self, query: str) -> List[Dict]:
        """Search Google Docs documents"""
        return await self.search_files(
            name=query,
            file_type="application/vnd.google-apps.document"
        )

    async def search_spreadsheets(self, query: str) -> List[Dict]:
        """Search Google Sheets"""
        return await self.search_files(
            name=query,
            file_type="application/vnd.google-apps.spreadsheet"
        )

    async def get_folder_contents(self, folder_id: str) -> List[Dict]:
        """Get all files in a specific folder"""
        return await self.list_files(folder_id=folder_id)


# Simple interface functions
async def list_my_files(max_results: int = 20) -> List[Dict]:
    """Quick function to list recent files"""
    drive = DriveIntegration()
    return await drive.get_recent_files(max_results)


async def search_drive(query: str) -> List[Dict]:
    """Quick function to search Drive"""
    drive = DriveIntegration()
    return await drive.search_files(name=query)


async def download_file_by_name(filename: str, output_path: str) -> bool:
    """Download a file by searching for its name"""
    drive = DriveIntegration()
    files = await drive.search_files(name=filename)

    if not files:
        logger.error(f"File not found: {filename}")
        return False

    # Download first match
    await drive.download_file(files[0]["id"], output_path)
    return True
