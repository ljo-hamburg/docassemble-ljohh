import base64
import io
import json
from typing import Any, Dict, Iterable

import requests
from docassemble.base.core import DAFile
from docassemble.base.functions import get_config
from docassemble.base.util import send_email
from google.oauth2 import service_account
from googleapiclient import discovery

__all__ = ["add_spreadsheet_row", "add_group_member"]

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def get_google_credentials(**kwargs):
    print("Getting Creds")
    info = get_config('google').get('service account credentials')
    return service_account.Credentials.from_service_account_info(
        json.loads(info, strict=False),
        **kwargs
    )


def add_spreadsheet_row(spreadsheet: str, range: str, data: Dict[str, Any]):
    credentials = get_google_credentials(
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet,
        range=range
    )
    response = request.execute()
    print("Response:")
    print(response)
    headers = response["values"][0]
    data = {key.casefold(): value for key, value in data.items()}
    row = list(map(lambda header: data.get(header.casefold(), None), headers))
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet,
        range=range,
        valueInputOption='RAW',
        insertDataOption='OVERWRITE',
        body={
            "majorDimension": "ROWS",
            "values": [row]
        }
    )
    request.execute()
    return True


def add_group_member(group: str, email: str):
    credentials = get_google_credentials(
        subject="admin@ljo-hamburg.de",  # Delegate to Domain Admin
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


def upload_file(file: DAFile):
    file.retrieve()
    credentials = get_google_credentials()
    service = discovery.build('drive', 'v3', credentials=credentials)
    file_metadata = {
        'name': file.filename
    }
    media = MediaFileUpload(file.path(), mimetype=file.mimetype)
    request = service.files().create(body=file_metadata, media_body=media)
    result = request.execute()
    print(result)
    return result


def send_member_mail():
    send_email(
        to=[mitglied],
        template=mitglied_email,
        attachments=[anmeldeformular, teilnahmebedingungen, geschäftsordnung]
    )


def send_orga_mail():
    recipients = anmeldeformular["E-Mail Benachrichtigung"]
    if not recipients:
        return
    send_email(
        to=recipients,
        template=orga_mail,
        attachments=[anmeldeformular]
    )


def archive_registration():
    requests.post(
        'https://script.google.com/macros/s/AKfycbzTVMyYn6q0OydgArzMbTBlw197-6B7uunHzPJp6Pn8d92wQQI/exec',
        data={
            'folderID': automation['archive folder'],
            'filename': registration.pdf.filename,
            'key': '8aPDVTmpRdzqxwP700QAgTqk9tUtAomm',
            'data': base64.b64encode(registration.pdf.slurp(auto_decode=False))
        }).raise_for_status()
