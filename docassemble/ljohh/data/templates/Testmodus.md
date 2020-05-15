<div class="alert alert-info" role="alert">
  <h5 class="alert-heading">Testmodus</h5>
  
  Die Anmeldung befindet sich im Testmodus. Daher werden keine E-Mails
  verschickt und auch keine weiteren Automatisierungen vorgenommen. Dies ist nur
  eine Zusammenfassung der Automatisierung, die bei einer echten Anmeldung
  ablaufen würde.
</div>

### Anmeldungsformular
Es wurde ein Anmeldungsformular als PDF generiert.

<a href="${ anmeldung.pdf.url_for() }"
   target="_blank"
   class="btn btn-primary btn-sm">
    Anmeldeformular ansehen
</a>

### Begrüßungs-E-Mail
Eine E-Mail würde an `${ mitglied.email }` geschickt werden. In der E-Mail wird
${ mitglied.name } zur Arbeitsphase begrüßt. Es werden außerdem wichtige
Randinformationen genannt. Der Text der E-Mail kann unten angesehen werden. Das
Design der E-Mail sieht allerdings anders aus.

An die E-Mail sind drei Dokumente angehängt:

- [${ anmeldeformular.pdf.filename }](${ anmeldung.pdf.url_for() })
- [${ teilnahmebedingungen.filename }](${ teilnahmebedingungen.url_for() })
- [${ geschaeftsordnung.filename }](${ geschaeftsordnung.url_for() })

<p>
  <%self:collapse_button id="mitglied-email-collapse">
    E-Mail-Inhalt anzeigen
  </%self:collapse_button>
  <%self:action_button action="send_member_email"
                       message="Die E-Mail wurde gesendet. Es kann einen Moment dauern, bis die Mail ankommt.">
    E-Mail trotzdem senden
  </%self:action_button>
</p>

<%self:collapse id="mitglied-email-collapse" title="${ mitglied_email.subject }">
  ${ mitglied_email }
</%self:collapse>

### Benachrichtigungs-E-Mail
Bei jeder Anmeldung werden bestimmte Empfänger benachrichtigt.
% if not daten["E-Mail Benachrichtigung"]:
Es sind bisher keine Empfänger konfiguriert, daher würde dieser Schritt
übersprungen werden.
% else:
Die Benachrichtigung enthält ebenfalls die
[Anmeldung](${ anmeldung.pdf.url_for() }) im Anhang, enhält aber nur wenig Text
und auch nicht die Teilnahmebedingungen und die Geschäftsordnung. Folgende
Empfänger werden benachrichtigt:

% for email in daten["E-Mail Benachrichtigung"]:
  - `${ email }`
% endfor

Wenn du unten auf "E-Mail trotzdem senden" klickst, wird die E-Mail im Testmodus
nur an die von dir angegebene Adresse `${ mitglied.email }` gesendet.

<p>
  <%self:collapse_button id="orga-email-collapse">
    E-Mail-Inhalt anzeigen
  </%self:collapse_button>
  <%self:action_button action="send_orga_email"
                       message="Die E-Mail wurde gesendet. Es kann einen Moment dauern, bis die E-Mail ankommt.">
    E-Mail trotzdem senden
  </%self:action_button>
</p>

<%self:collapse id="orga-email-collapse" title="${ orga_email.subject }">
  ${ orga_email }
</%self:collapse>
% endif

### Archivieren der Anmeldung
Das Anmeldeformular wird automatisch in einem Google Drive Ordner mit der ID
`${ test_archiv_ordner['id'] }` archiviert.

${ check_folder(test_archiv_ordner) }

<p>
  <%self:action_button action="archive_registration"
                       message="Die Anmeldung wurde zum Ordner hinzugefügt.">
    Anmeldung archivieren
  </%self:action_button>
  <a class="btn btn-secondary btn-sm"
     target="_blank"
     href="https://drive.google.com/drive/u/0/folders/${ test_archiv_ordner['id'] }">Ordner öffnen</a>
</p>

### Mailingliste
Die E-Mail-Adresse `${ mitglied.email }` wird dem Verteiler
`${ test_mitglied_mailingliste['email'] }` hinzugefügt.

${ check_group(test_mitglied_mailingliste) }

<%self:action_button action="register_email"
                     email="${ mitglied.email }"
                     group="${ test_mitglied_mailingliste['email'] }"
                     message="Die E-Mail ${ mitglied.email } wurde zur Gruppe hinzugefügt.">
  Zur Gruppe hinzufügen
</%self:action_button>

### Mailingliste (Eltern)
% if minderjaehrig:
Die E-Mail-Adresse `${ eltern.email }` wird dem Verteiler
`${ test_eltern_mailingliste['email'] }` hinzugefügt.
% else:
${ mitglied.name } ist volljährig. Daher wird keine Elternadresse zur
Mailingliste hinzugefügt. Der Elternverteiler ist
`${ test_eltern_mailingliste['email'] }`.
% endif

${ check_group(test_eltern_mailingliste) }

% if minderjaehrig:
<%self:action_button action="register_email"
                     email="${ eltern.email }"
                     group="${ test_eltern_mailingliste['email'] }"
                     condition="${ minderjaehrig }"
                     message="Die E-Mail ${ eltern.email } wurde zur Gruppe hinzugefügt.">
  Zur Gruppe hinzufügen
</%self:action_button>
% endif

### Anmeldeliste
Alle eingegebenen Daten werden automatisch zur Anmeldeliste hinzugefügt. Die
Anmeldeliste ist eine Google-Tabelle mit der ID
`${ test_anmeldungen_tabelle["id"] }`. Die Daten werden dort dem Bereich
`${ daten["Anmeldungen"]["Bereich"] }` hinzugefügt. Überschriften werden
automatisch erkannt und den Einträgen zugeordnet.

${ check_spreadsheet(test_anmeldungen_tabelle) }

<p>
  <%self:action_button action="append_to_spreadsheet"
                       spreadsheet="${ test_anmeldungen_tabelle['id'] }"
                       range="${ daten['Anmeldungen']['Bereich'] }"
                       message="Die Daten wurden zur Anmeldeliste hinzugefügt.">
    Zur Tabelle hinzufügen
  </%self:action_button>
  <a class="btn btn-secondary btn-sm"
     target="_blank"
     href="https://docs.google.com/spreadsheets/d/${ test_anmeldungen_tabelle['id'] }/edit#gid=daten['Anmeldungen']['Blatt-ID']">Tabelle öffnen</a>
</p>
