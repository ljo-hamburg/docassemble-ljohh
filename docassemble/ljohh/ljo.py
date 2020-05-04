import json
from typing import Any, Dict

from bs4 import BeautifulSoup
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
    normalized_data = {key.casefold(): value for key, value in data.items()}
    row = [normalized_data.get(header.casefold(), None) for header in headers]
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


def send_ljo_email(to, template, attachments=None, mg_template=None):
    html = template.content_as_html()
    body = BeautifulSoup(html, "html.parser").get_text('\n')
    mg_vars = {}
    if mg_template:
        mg_vars["template"] = mg_template
        mg_vars["content"] = template.content_as_html()
    return send_email(
        to=to,
        body=body,
        subject=template.subject,
        attachments=attachments,
        mailgun_variables=mg_vars
    )
