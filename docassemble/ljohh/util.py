from docassemble.base.error import DAError
from docassemble.base.functions import value
from docassemble.base.util import Address, format_date, Person


def da_error(value, code=500):
    raise DAError(value, code=code)


def FakeTask():
    def ready():
        return True


def max_fehltermine(key, anzahl):
    """
    Berechnet die Anzahl der Präsenztermine, sodass höchstens anzahl Fehltermine
    verzeichnet sind. Wenn status != "mitglied" ist, wird immer 0 zurückgegeben.
    """
    config: dict = value("daten")
    if value("status") == "mitglied":
        return len(config[key]) - anzahl
    else:
        return 0


def alle_termine(key):
    """
    Erstellt eine Checkbox-Liste mit den Terminen in der entsprechenden
    Konfiguration.
    """
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


def ja_nein_vielleicht(*args):
    """
    Ohne Argumente erstellt diese Funktion eine Ja-Nein-Vielleicht Auswahl. Mit
    einem Argument gibt es den Wert der entsprechenden Auswahl zurück.
    """
    values = {
        True: "Vermutlich ja",
        False: "Vermutlich nein",
        None: "Kann ich noch nicht sagen"
    }
    if args:
        return values[args[0]]
    else:
        return [
            {True: values[True]},
            {False: values[False]},
            {None: values[None]}
        ]


def terminliste():
    """
    Erstellt eine Liste von Terminen, in denen Fehltermine gekennzeichnet sind.
    Das Ergebnis kann dem Benutzer angezeigt werden.
    """
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


def get_pwe_versorgung():
    """
    Erstellt eine Liste mit allen Angaben zur Versorgung beim Probenwochenende.
    """
    versorgung: dict = value('pwe_versorgung')
    angaben = []
    if versorgung.get('vegan'):
        angaben.append("Ich möchte **vegan** versorgt werden.")
    elif versorgung.get('vegetarisch'):
        angaben.append("Ich möchte **vegetarisch** versorgt werden.")
    return angaben


def pwe_angaben():
    """
    Gibt einen wahren Wert zurück, wenn irgendwelche Angaben zum
    Probenwochenende gemacht wurden.
    """
    return get_pwe_versorgung() or value('pwe_sonstiges').strip()


def alle_fehltermine():
    """
    Gibt eine Liste von Daten zurück, die als Fehltermin gekennzeichnet wurden.
    """
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
    """
    Gibt True zurück, wenn die Person in der angegebenen Phase weiterhin
    mitspielt.
    """
    return phase is True


def nicht_dabei(phase):
    """
    Gibt True zurück, wenn die Person in der angegebenen Phase nicht mehr
    mitspielt.
    """
    return phase is False


def unsicher(phase):
    """
    Gibt True zurück, wenn die Person nicht sicher ist, ob sie in der
    angegebenen Phase weiter mitspielt.
    """
    return phase is None


def adresse(thing):
    """
    Gibt eine formatierte Postadresse zurück.
    """
    if isinstance(thing, str):
        return thing
    if isinstance(thing, Person):
        address = thing.address
    elif isinstance(thing, Address):
        address = thing
    else:
        raise ValueError(f"Cannot format object of type {type(thing)}")
    components = []
    if getattr(address, "route", None) and getattr(address, "street_number", None):
        components.append(f"{address.route} {address.street_number}")
    elif getattr(address, "route", None):
        components.append(address.route)
    elif address.address:
        components.append(address.address)
    city_components = []
    if getattr(address, "zip", None):
        city_components.append(address.zip)
    if getattr(address, "city", None):
        city_components.append(address.city)
    components.append(" ".join(city_components))
    return ", ".join(components)
