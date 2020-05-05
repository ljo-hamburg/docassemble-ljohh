<%def name="check_table(table)">
% if table["code"] == 404:
  <span style="color:red">
  Diese Tabelle wurde nicht gefunden. Prüfe, ob die ID richtig ist und ob der
  Account ${ daten["Account"] } Zugriff auf die Datei hat.
  </span>
% elif table["code"] == 403:
  <span style="color:red">
  Der Account ${ daten["Account"] } hat keinen Zugriff auf die Tabelle.
  </span>
% elif table["code"] == 200:
  - ⇒ **${ table["name"] }**

% if not table["sheet"]:
  <span style="color:red">
  Die Datei ist keine Google Tabelle.
  </span>
% elif not table["editable"]:
  <span style="color:red">
  Der Account ${ daten["Account"] } kann keine Daten in die Tabelle
  schreiben.
  </span>
% endif
% else:
<span style="color:red">
Ein unbekannter Fehler ist aufgetreten.
</span>
% endif
</%def>
<%def name="check_group(group)">
% if group["code"] == 404:
  <span style="color:red">
  Die Gruppe exitiert nicht.
  </span>
% elif group["code"] == 200:
  - ⇒ **${ group["name"] }**
% else:
  <span style="color:red">
  Ein unbekannter Fehler ist aufgetreten.
  </span>
% endif
</%def>
<%def name="check_folder(folder)">
% if folder["code"] == 404:
  <span style="color:red">
  Der Ordner wurde nicht gefunden. Prüfe, ob die ID richtig ist und ob der
  Account ${ daten["Account"] } Zugriff auf den Ordner hat.
  </span>
% elif folder["code"] == 403:
  <span style="color:red">
  Der Account ${ daten["Account"] } hat keinen Zugriff auf den Ordner.
  </span>
% elif folder["code"] == 200:
  - ⇒ **${ folder["name"] }**

% if not folder["folder"]:
  <span style="color:red">
  Die ID ist kein Ordner.
  </span>
% elif not folder["editable"]:
  <span style="color:red">
  Der Account ${ daten["Account"] } kann keine Daten in den Ordner
  schreiben.
  </span>
% endif
% else:
<span style="color:red">
Ein unbekannter Fehler ist aufgetreten.
</span>
% endif
</%def>

Die Anmeldung befindet sich im Testmodus. Daher werden keine E-Mails
verschickt und auch keine weiteren Automatisierungen vorgenommen. Außerhalb
des Testmodus würde nun folgendes passieren:

1. Die eingegebenen Daten werden in der Tabelle mit der ID
 `${ test_anmeldungen_tabelle["id"] }` eingetragen.

 ${ check_table(test_anmeldungen_tabelle) }
2. Die eingegebenen Daten werden in der Mitgliedertabelle mit der ID
 `${ test_mitglieder_tabelle["id"] }` eingetragen.

 ${ check_table(test_mitglieder_tabelle) }
3. Die E-Mail-Adresse ${ mitglied.email } wird dem Verteiler
 ${ test_mitglied_mailingliste["email"] } hinzugefügt.

 ${ check_group(test_mitglied_mailingliste) }
% if minderjaehrig:
4. Die E-Mail-Adresse ${ eltern.email } wird dem Verteiler
   ${ test_eltern_mailingliste["email"] } hinzugefügt.

   ${ check_group(test_eltern_mailingliste) }
% endif
5. Das Anmeldeformular wird im Ordner mit der ID `${ test_archiv_ordner["id"] }`
 gespeichert.

 ${ check_folder(test_archiv_ordner) }
7. Eine E-Mail wird an ${ mitglied.email } gesendet. Die E-Mail ist unten zu
 sehen. Angehängt an die E-Mail sind das Anmeldeformular, die
 Teilnahmebedingungen und die Geschäftsordnung.
% if daten["E-Mail Benachrichtigung"]:
8. Die folgenden Empfänger werden per E-Mail über die Anmeldung benachrichtigt
 und erhalten die Anmeldung im Anhang:

 % for email in daten["E-Mail Benachrichtigung"]:
  - ${ email }
 % endfor
% endif

% if daten["E-Mail Benachrichtigung"]:
### E-Mail: *${ orga_email.subject }*
Diese E-Mail wird als Benachrichtigung versendet, wenn eine Anmeldung
abgeschickt wird.

<div class="card card-body">
${ orga_email }
</div>
% endif

### E-Mail: *${ mitglied_email.subject }*
Diese E-Mail wird an ${ mitglied.name } gesendet. Der Inhalt der E-Mail
ist in diesem PDF zu sehen, das Design sieht aber anders aus. Angehängt an
diese Mail sind die folgenden Dokumenten:

- [${ anmeldeformular.pdf.filename }](${ anmeldung.pdf.url_for() })
- [${ teilnahmebedingungen.filename }](${ teilnahmebedingungen.url_for() })
- [${ geschaeftsordnung.filename }](${ geschaeftsordnung.url_for() })

<div class="card card-body">
${ mitglied_email }
</div>