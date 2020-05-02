import base64
import json

import requests
from docassemble.base.functions import get_config
from docassemble.base.util import send_email
from google.oauth2 import service_account
from googleapiclient import discovery

__all__ = ["add_spreadsheet_row", "add_group_member"]


def get_google_credentials(**kwargs):
    info = get_config('google').get('service account credentials')
    return service_account.Credentials.from_service_account_info(
        json.loads(info, strict=False),
        **kwargs
    )


def add_spreadsheet_row(spreadsheet: str, range: str, data: dict):
    credentials = get_google_credentials(
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    request = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet,
        range=range
    )
    headers = request.execute()[0]
    row = map(lambda header: data.get(header, None), headers)
    request = service.spreadsheet().values().append(
        spreadsheetId=spreadsheet,
        range=range,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
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
    request.execute()
    return True


def send_member_mail():
    send_email(
        to=[mitglied],
        template=mitglied_mail,
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


def raw_dates(date_list):
    return [date[0] if isinstance(date, tuple) else date for date in date_list]


def missing_dates():
    dates = []
    for date in raw_dates(rehearsals + concerts + tour):
        if not rehearsal_dates.get(date, False) and \
                not concert_dates.get(date, False) and \
                not tour_dates.get(date, False):
            dates.append(date)
    return dates


def yesnomaybe(x):
    if x is None:
        return "maybe"
    elif x:
        return "yes"
    else:
        return "no"
