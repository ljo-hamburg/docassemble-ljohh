from docassemble.base.functions import value
from docassemble.base.util import format_date, validation_error


def max_fehltermine(key, amount):
    config: dict = value("daten")
    if value("status") == "normal":
        return len(config[key]) - amount
    else:
        return 0


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


def ja_nein_vielleicht():
    return [
        {True: "Vermutlich ja"},
        {False: "Vermutlich nein"},
        {None: "Kann ich noch nicht sagen"}
    ]


def terminliste():
    output = ""
    config: dict = value("daten")
    probentermine: dict = value("probentermine")
    konzerttermine: dict = value("konzerttermine")
    for date in config["Probentermine"] + config["Konzerttermine"]:
        the_date = date[0] if isinstance(date, list) else date
        text = format_date(the_date, 'E, d. MMMM yyyy')
        if isinstance(date, list):
            text += " (" + date[1] + ")"
        if probentermine.get(the_date, False) \
                or konzerttermine.get(the_date, False):
            output += "- " + text + "\n"
        else:
            output += '- <span style="color: red; ' \
                      'text-decoration: line-through">' + text + '</span>\n'
    return output


def alle_pwe_angaben():
    versorgung: dict = value('pwe_versorgung')
    sonstiges: str = value('pwe_sonstiges')
    angaben = []
    if versorgung.get('vegan'):
        angaben.append("Ich möchte **vegan** versorgt werden.")
    elif versorgung.get('vegetarisch'):
        angaben.append("Ich möchte **vegetarisch** versorgt werden.")
    angaben.extend(
        line.strip() for line in sonstiges.splitlines() if line.strip()
    )
    return angaben


def alle_fehltermine():
    config: dict = value("daten")
    probentermine = value("probentermine")
    konzerttermine = value("konzerttermine")
    dates = []
    for date_value in config["Probentermine"] + config["Konzerttermine"]:
        date = date_value[0] if isinstance(date_value, list) else date_value
        if not probentermine.get(date, False) and \
                not konzerttermine.get(date, False):
            dates.append(date)
    return dates


def dabei(phase):
    return phase is True


def nicht_dabei(phase):
    return phase is False


def unsicher(phase):
    return phase is None
