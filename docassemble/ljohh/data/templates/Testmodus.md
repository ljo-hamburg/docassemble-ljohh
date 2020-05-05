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

<div>
    ${ collapse_button(
           'mitglied-email-collapse',
           'E-Mail-Inhalt anzeigen',
           css_class='btn-sm'
       ) }
    <button type="button"
            id="send-mitglied-mail-button"
            class="btn btn-primary btn-sm">
    E-Mail trotzdem senden
    </button>
</div>

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
  - ${ email }
% endfor

${ collapse_button(
       'orga-email-collapse',
       'E-Mail-Inhalt anzeigen',
       css_class='btn-sm'
   ) }
<button type="button"
        id="send-orga-mail-button"
        class="btn btn-primary btn-sm">
E-Mail trotzdem senden
</button>

<%self:collapse id="orga-email-collapse" title="${ orga_email.subject }">
  ${ orga_email }
</%self:collapse>
% endif

### Archivieren der Anmeldung
Das Anmeldeformular wird automatisch in einem Google Drive Ordner mit der ID
`${ test_archiv_ordner['id'] }` archiviert.

${ check_folder(test_archiv_ordner) }

<button type="button"
        id="archive-registration-button"
        class="btn btn-primary btn-sm">
Anmeldung archivieren
</button>

### Mailingliste
Die E-Mail-Adresse `${ mitglied.email }` wird dem Verteiler
`${ test_mitglied_mailingliste['email'] }` hinzugefügt.

${ check_group(test_mitglied_mailingliste) }

<button type="button"
        id="register-member-mail-button"
        class="btn btn-primary btn-sm">
Zur Gruppe hinzufügen
</button>

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
<button type="button"
        id="register-parent-mail-button"
        class="btn btn-primary btn-sm">
E-Mail trotzdem senden
</button>
% endif

### Anmeldeliste
Alle eingegebenen Daten werden automatisch zur Anmeldeliste hinzugefügt. Die
Anmeldeliste ist eine Google-Tabelle mit der ID
`${ test_anmeldungen_tabelle["id"] }`. Die Daten werden dort dem Bereich
`${ daten["Anmeldungen"]["Bereich"] }` hinzugefügt. Überschriften werden
automatisch erkannt und den Einträgen zugeordnet.

${ check_spreadsheet(test_anmeldungen_tabelle) }

<button type="button"
        id="save-data-button"
        class="btn btn-primary btn-sm">
Zur Tabelle hinzufügen
</button>

### Mitgliederliste
Alle Daten werden auch automatisch zur Mitgliederliste hinzugefügt. Die
Mitgliederliste ist mit der ID `${ test_mitglieder_tabelle["id"] }` konfiguriert.
Dort werden Daten im Bereich `${ daten["Mitgliederliste"]["Bereich"] }`
hinzugefügt. Überschriften werden automatisch erkannt und den Einträgen
zugeordnet.

 ${ check_spreadsheet(test_mitglieder_tabelle) }

<button type="button"
        id="add-member-button"
        class="btn btn-primary btn-sm">
Zur Tabelle hinzufügen
</button>
