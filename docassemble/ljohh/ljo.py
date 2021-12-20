import json
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup
from docassemble.base.core import DAFile
from docassemble.base.util import email_stringer, send_email, mark_task_as_performed, get_config, value
from flask_mail import sanitize_addresses
from google.oauth2 import service_account
from googleapiclient import discovery

__all__ = [
    "ljo_account",
    "get_group_meta",
    "add_group_member",
    "upload_file",
]

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from requests.auth import HTTPBasicAuth


def ljo_account():
    """
    Returns the email address of the service account that is used for
    automation actions.
    """
    info = get_config('google').get('service account credentials')
    data = json.loads(info, strict=False)
    return data["client_email"]


def get_google_credentials(**kwargs):
    """
    Returns Credentials that are able to authenticate against the Google APIs.
    Use the keyword arguments to provide further details (such as the scopes of
    the credentials).
    """
    info = get_config('google').get('service account credentials')
    return service_account.Credentials.from_service_account_info(
        json.loads(info, strict=False),
        **kwargs
    )

def get_group_meta(group: str):
    """
    Returns information about the specified group.
    """
    credentials = get_google_credentials(
        scopes=["https://www.googleapis.com/auth/admin.directory.group.readonly"]
    )
    service = discovery.build('admin', 'directory_v1', credentials=credentials)
    request = service.groups().get(
        groupKey=group
    )
    try:
        response = request.execute()
        return {
            "code": 200,
            "email": response["email"],
            "name": response["name"]
        }
    except HttpError as error:
        if error.resp.status == 404:
            return {
                "email": group,
                "code": 404
            }
        raise error


def add_group_member(group: str, email: str):
    """
    Adds a member to a group. Both are specified using the respective email
    address.
    """
    credentials = get_google_credentials(
        scopes=["https://www.googleapis.com/auth/admin.directory.group.member"],
    )
    service = discovery.build('admin', 'directory_v1', credentials=credentials)
    request = service.members().insert(
        groupKey=group,
        body={
            "email": email,
            "role": "MEMBER"
        }
    )
    try:
        request.execute()
    except HttpError as error:
        # If the email is already in the group do not raise an error.
        # Status code 409 Conflict
        if error.resp.status != 409:
            raise error
    return True


def upload_file(file: DAFile, folder: str):
    """
    Uploads a file into the specified folder. The folder is specified using its
    ID.
    """
    file.retrieve()
    credentials = get_google_credentials(
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = discovery.build('drive', 'v3', credentials=credentials)
    file_metadata = {
        'name': file.filename,
        'parents': [folder]
    }
    media = MediaFileUpload(file.path(), mimetype=file.mimetype)
    request = service.files().create(
        supportsAllDrives=True,
        body=file_metadata,
        media_body=media)
    request.execute()
    return True
