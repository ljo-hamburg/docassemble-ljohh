__all__ = [
    "ljo_account",
    "get_group_meta",
    "add_group_member",
]

import json

from docassemble.base.util import get_config
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError


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
    delegate = get_config('google').get('delegated admin')
    return service_account.Credentials.from_service_account_info(
        json.loads(info, strict=False),
        **kwargs
    ).with_subject(delegate)


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
        return request.execute()
    except HttpError as error:
        return json.loads(error.content)


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
