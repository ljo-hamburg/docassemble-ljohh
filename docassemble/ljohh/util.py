from docassemble.base.functions import value
from docassemble.base.util import format_date, validation_error


def alle_termine(key):
    config: dict = value("daten")
    return [
        {
            date[0]: format_date(date[0], 'E, d. MMMM'),
            'default': True,
            'help': date[1]
        } if isinstance(date, list) else {
            date: format_date(date, 'E, d. MMMM'),
            'default': True
        } for date in config[key]
    ]


def fehltermine(key, amount):
    config: dict = value("daten")
    if value("status") == "normal":
        return len(config[key]) - amount
    else:
        return 0


def ja_nein_vielleicht():
    return [
        {True: "Vermutlich ja"},
        {False: "Vermutlich nein"},
        {None: "Kann ich noch nicht sagen"}
    ]


def terminliste():
    output = ""
    config: dict = value("daten")
    rehearsal_dates: dict = value("probentermine")
    concert_dates: dict = value("konzerttermine")
    for date in config["Probentermine"] + config["Konzerttermine"]:
        the_date = date[0] if isinstance(date, list) else date
        text = format_date(the_date, 'E, d. MMMM yyyy')
        if isinstance(date, list):
            text += " (" + date[1] + ")"
        if rehearsal_dates.get(the_date, False) \
                or concert_dates.get(the_date, False):
            output += "- " + text + "\n"
        else:
            output += '- <span style="color: red; ' \
                      'text-decoration: line-through">' + text + '</span>\n'
    return output


def pwe_angaben():
    pwe_other: str = value('pwe_sonstiges')
    return [line.strip() for line in pwe_other.splitlines() if line.strip()]


def dabei(phase):
    return phase is True


def nicht_dabei(phase):
    return phase is False


def unsicher(phase):
    return phase is None
