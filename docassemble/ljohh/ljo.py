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
    "get_file_meta",
    "get_group_meta",
    "add_spreadsheet_row",
    "add_group_member",
    "upload_file",
    "send_ljo_email"
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


def get_file_meta(file: str, mode: str = None, **kwargs):
    """
    Returns information about the file with the specified ID. Optionally
    additional information can be queried using the mode parameter. Currently
    the only supported value is 'spreadsheet'. If mode is set to 'spreadsheet'
    you must provide an additional keyword argument 'range' specifying the range
    where data would be inserted.
    """
    scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    if mode == "spreadsheet":
        scopes.append(
            "https://www.googleapis.com/auth/spreadsheets.readonly")
    credentials = get_google_credentials(
        scopes=scopes
    )
    service = discovery.build('drive', 'v3', credentials=credentials)
    request = service.files().get(
        fileId=file,
        supportsAllDrives=True,
        fields="id,"
               "name,"
               "mimeType,"
               "capabilities/canEdit,"
               "capabilities/canModifyContent"
    )
    try:
        result = request.execute()
        meta = {
            "code": 200,
            "id": result["id"],
            "name": result["name"],
            "editable": result["capabilities"]["canEdit"]
                        and result["capabilities"]["canModifyContent"],
            "sheet": result[
                         "mimeType"] == "application/vnd.google-apps.spreadsheet",
            "folder": result["mimeType"] == "application/vnd.google-apps.folder"
        }
    except HttpError as error:
        if error.resp.status in {403, 404}:
            return {
                "id": file,
                "code": error.resp.status
            }
        else:
            raise error
    if mode == "spreadsheet":
        service = discovery.build('sheets', 'v4', credentials=credentials)
        request = service.spreadsheets().values().get(
            spreadsheetId=file,
            range=kwargs["range"]
        )
        try:
            result = request.execute()
            meta["range"] = result["range"]
        except HttpError as error:
            if error.resp.status == 400:
                meta["range"] = False
            else:
                raise error
    return meta


def add_spreadsheet_row(spreadsheet: str, range: str, data: Dict[str, Any]):
    """
    Inserts a new row of data into the spreadsheet with the specified ID in the
    specified range. The data dictionary provides the data. Keys in the
    dictionary are matched against the first row in the range (usually a header
    row of the table) to determine which fields should be inserted where. The
    comparison is performed case-insensitively.
    """
    credentials = get_google_credentials(
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet,
        range=range
    )
    response = request.execute()
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
    response = request.execute()
    return True


def get_group_meta(group: str):
    """
    Returns information about the specified group.
    """
    credentials = get_google_credentials(
        subject="admin@ljo-hamburg.de",  # Delegate to Domain Admin
        scopes=[
            "https://www.googleapis.com/auth/admin.directory.group.readonly"]
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


def send_ljo_email(
        to=None,
        sender=None,
        cc=None,
        bcc=None,
        body=None,
        html=None,
        subject="",
        template=None,
        task=None,
        attachments: List[DAFile] = None,
        mailgun_variables=None
):
    """
    Sends an email. This method is a drop-in replacement for docassemble's
    send_mail function. However this method will send the email using a
    pre-configured Mailgun template if possible. If not it falls back to the
    send_mail function.

    The template can be configured in the interview configuration as
    daten['Mailgun Vorlage'].
    """
    config = get_config('mail')
    url = config.get('mailgun send url',
                     "https://api.mailgun.net/v3/%s/messages")
    domain = config.get('mailgun domain', None)
    key = config.get('mailgun api key', None)
    mg_template = value('daten').get('Mailgun Vorlage', None)
    if not all([url, domain, key, mg_template]):
        return send_email(
            to=to,
            sender=sender,
            cc=cc,
            bcc=bcc,
            body=body,
            html=html,
            subject=subject,
            template=template,
            task=task,
            attachments=attachments,
            mailgun_variables=mailgun_variables
        )

    def join_email(email):
        return ", ".join(sanitize_addresses(email_stringer(email,
                                                           include_name=True)))

    html = html or template.content_as_html()
    text = body or BeautifulSoup(html, "html.parser").get_text('\n')
    data = {
        "from": sender or config["default sender"],
        "to": join_email(to),
        "subject": subject or template.subject,
        "template": mg_template,
        "text": text,
        "v:content": html
    }
    if cc:
        data["cc"] = join_email(cc)
    if bcc:
        data["bcc"] = join_email("bcc")
    if attachments:
        files = tuple(("attachment", (attachment.filename,
                                      attachment.slurp(auto_decode=False),
                                      attachment.mimetype))
                      for attachment in attachments)
    else:
        files = ()
    requests.post(url % domain,
                  auth=HTTPBasicAuth('api', key),
                  data=data,
                  files=files).raise_for_status()
    if task is not None:
        mark_task_as_performed(task)
    return True
