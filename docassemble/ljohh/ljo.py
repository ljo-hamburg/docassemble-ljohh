import base64

import requests
from docassemble.base.util import DADict, DAFile, DATemplate, Individual, \
    send_email

# Variables defined in interview files

def save_user_data():
    data = {
        'state': state,
        'firstName': mitglied.name.first,
        'lastName': mitglied.name.last,
        'mail': mitglied.email,
        'phone': mitglied.phone_number,
        'address': mitglied.address,
        'birthday': format_date(mitglied.birthdate, 'yyyy-MM-dd'),
        'instrument': mitglied.instrument,
        'rehearsals': list(rehearsal_dates.true_values()),
        'concerts': list(concert_dates.true_values()),
        'tour': list(tour_dates.true_values()),
        'nextTerm': yesnomaybe(next_term),
        'nextNextTerm': yesnomaybe(nextnext_term),
        'rendsburgNotes': list(rendsburg_notes.true_values()),
        'rendsburgExtendedNotes': rendsburg_extended_notes,
    }
    if person.age_in_years() < 18:
        data['parentFirstName'] = parent.name.first
        data['parentLastName'] = parent.name.last
        data['parentMail'] = parent.email
        data['parentPhone'] = parent.phone_number
    requests.post(
        'https://script.google.com/macros/s/AKfycbyWbQUObPHQGcv8-f1x6ynVX2kZHL4Y2hheOMXpgbAmVUxNCOk/exec',
        data={
            'spreadsheetID': automation['spreadsheet id'],
            'key': 'cHwzP9DaMbT8DWJIeuTulrPTwqGr7TWm',
            'data': json.dumps(data)
        }).raise_for_status()
    return True  # TODO: Return success/failed


def save_contact_data():
    contact_data = {
        'firstName': person.name.first,
        'lastName': person.name.last,
        'mail': person.email,
        'phone': person.phone_number,
        'address': person.address,
        'birthday': format_date(person.birthdate, 'yyyy-MM-dd'),
        'instrument': person.instrument,
        'group': automation['contact group'],
        'key': 'UUYxwdbAM6wqZ3NagCCbDpiGRXMtFuRU'
    }
    if person.age_in_years() < 18:
        contact_data['parentFirstName'] = parent.name.first
        contact_data['parentLastName'] = parent.name.last
        contact_data['parentMail'] = parent.email
        contact_data['parentPhone'] = parent.phone_number
    requests.post(
        'https://script.google.com/macros/s/AKfycbythVM4a1_dfHc6-JnY-YsauhfUwfD-JcK4-qHkAMDB96zrSEo/exec',
        data=contact_data).raise_for_status()
    return True  # TODO: Return success/failed


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


def register_member_email():
    requests.post(
        'https://script.google.com/macros/s/AKfycbw7xJlo62WldzOT9pbIUO-59EEfw70U7WUcPBO5KwFuMOUnTwc/exec',
        data={
            'user': person.email,
            'group': automation['mailing list'],
            'key': 'yARJdazgU77oJRySiBGcQy39mNpreO4k'
        }).raise_for_status()


def register_parent_email():
    if person.age_in_years() < 18:
        requests.post(
            'https://script.google.com/macros/s/AKfycbw7xJlo62WldzOT9pbIUO-59EEfw70U7WUcPBO5KwFuMOUnTwc/exec',
            data={
                'user': parent.email,
                'group': automation['parent mailing list'],
                'key': 'yARJdazgU77oJRySiBGcQy39mNpreO4k'
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
