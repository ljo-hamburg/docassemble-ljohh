# LJO-Anmeldungen

In diesem Repository befinden sich die [Online-Anmeldungen](https://anmeldung.ljo-hamburg.de) des LJO Hamburg. Die Online-Anmeldungen erlauben das automatische Erstellen von PDFs, die nur noch unterschrieben werden müssen.

## Überblick über den Anmeldeprozess

Der Anmeldeprozess kann beliebig komplex werden. Im Regelfall werden aber folgende Schritte ausgeführt:

1. Der Benutzer füllt auf der [Website](https://anmeldung.ljo-hamburg.de) das Anmeldeformular aus. Dabei wird nach persönlichen Daten, Terminkonflikten usw. gefragt. Es gibt auch die Möglichkeit eigene Kommentare anzugeben.
2. Der Benutzer klickt auf “abschicken”. Dadurch werden die eingegebenen Daten automatisch gespeichert (mehr dazu unten). Der Benutzer erhält eine E-Mail und kann das generierte Anmeldeformular herunterladen.
3. Das Formular wird unterschrieben und abgegeben. Dies ist passiert jedoch außerhalb des Anmeldeprozesses.

Das automatische Speichern von Daten besteht aus den folgenden Schritten:

- Hinzufügen der Daten zu einer Anmeldeliste (ein Google Sheet)
- Hinzufügen der E-Mail-Adresse des Benutzers (sowie ggf. der Eltern) zu einer Mailingliste (Google Groups)
- Abspeichern des Anmeldeformulars in einem Google Drive Ordner.
- Schicken einer Begrüßungsmail an den Benutzer mit Anmeldung, Teilnahmebedingungen und Geschäftsordnung im Anhang.
- Schicken einer Info-Mail an vorgegebene Adressen mit der Anmeldung im Anhang.

## Neue Anmeldungen erstellen

### Automatisierung vorbereiten

Um die automatischen Anmeldungen zu nutzen, müssen einige Dinge vorbereitet werden:

1. Erstellen eines Ordners in Google Drive, in dem die generierten PDFs gespeichert werden. Der Ordner muss mit dem Account `anmeldung@docassemble-264719.iam.gserviceaccount.com` freigegeben werden. Der Account benötigt Schreibzugriff auf den Ordner.
   
   Befindet sich der Ordner in einer Geteilten Ablage, muss der Account Mitglied der Geteilten Ablage werden.
   
2. Erstellung einer Google-Tabelle, in der die Anmeldedaten gespeichert werden. Der Account `anmeldung@docassemble-264719.iam.gserviceaccount.com` muss mit Schreibzugriff zu der Tabelle hinzugefügt werden. In der Tabelle muss es einen Bereich geben, in dem neue Daten hinzugefügt werden sollen. Der Bereich muss in seiner ersten Zeile Überschriften enthalten. Neue Einträge werden am logischen Ende der Tabelle hinzugefügt. Der Bereich kann per A1-Notation oder als benannter Bereich angegeben werden.

   Die Überschriften können nicht willkürlich sein. Anhand der Überschriften werden die dazugehörigen Daten gefunden. Die Überschriften entsprechen den Schlüsseln im `member_data`-Dictionary, das in `tasks.yml` definiert wird.

3. Erstellen von zwei Mailinglisten, in denen Mitglieder-E-Mails und Eltern-E-Mails gespeichert werden sollen. Hier muss nichts weiter konfiguriert werden, damit automatische Anmeldungen funktionieren.

4. Bearbeiten der Interview- und Template-Dateien (s.u.)

### Anmeldungen bearbeiten

Das Erstellen und Bearbeiten von Anmeldungen wird über `.yml`-Dateien konfiguriert. Im Wesentlichen sind hier zwei Dateien relevant:

- `docassemble/ljohh/data/questions/<anmeldung>.yml`: Dies ist der Einstiegspunkt  für die Anmeldung. Hier wird die Anmeldung konfiguriert.
- `docassemble/ljohh/data/questions/<anmeldung>-fragen.yml`: Hier befindet sich der Inhalt der Anmeldung (also die Texte, die der Nutzer sieht). Diese Datei muss für eine neue Anmeldung deutlich bearbeitet werden.

Darüber hinaus sind die folgenden Dateien relevant:

- `docassemble/ljohh/data/templates/<Anmeldung>.docx`: Dies ist die Vorlage für das Anmeldeformular.
- `docassemble/ljohh/data/templates/E-Mail <..>.md` und `docassemble/ljohh/data/templates/Benachrichtigung.md`: Diese beiden Dateien enthalten den Inhalt der E-Mails, die an den Benutzer bzw. als Benachrichtigung geschickt werden.

Zum Erstellen einer neuen Anmeldung ist es i.d.R. am einfachsten, die existierenden Dateien zu kopieren und zu bearbeiten. In den `.yml`-Dateien sind Kommentare (Zeilen, die mit `#` beginnen) enthalten, die die einzelnen Konfigurationen näher erläutern. Siehe auch:

- [YAML (Wikipedia)](https://de.wikipedia.org/wiki/YAML)
- [Markdown (Wikipedia)](https://de.wikipedia.org/wiki/Markdown)

## Hinter den Kulissen

Das Anmeldesystem ist in [docassemble](https://docassemble.org) geschrieben. Für ein besseres Verständnis sollte man zuerst die [docassemble-Übersicht](https://docassemble.org/docs.html) durchlesen. Im Weiteren wird davon ausgegangen, dass die docassemble-Grundbegriffe bekannt sind.

In der Startdatei `<anmeldung>.yml` sind im Wesentlichen Konfigurationen definiert, die in den anderen Dateien verwendet werden. Hier ist außerdem ein `mandatory` code block, der den Ablauf des Interviews bestimmt. Der Block fragt Variablen ab, die den `field`s in der `<anmeldung>-fragen.yml` definiert sind (sodass die entsprechenden Fragen in der angegebenen Reihenfolge gestellt werden). Es gibt einige spezielle Fragen:

-  `Kontrolle` ist eine `review`-Frage, die es möglich macht, vorherige Antworten zu bearbeiten. Dies ist ein Feature von docassemble.
- `Abschicken` ist eine spezielle Variable, die in `data.yml` definiert ist. Dadurch wird das automatische Abspeichern ausgelöst (s.u.).
- `Testergebnisse` und `Fertig` sind `event`s, die einen `exit`-Button anbieten und das Interview beenden. Es gibt keine weiteren `mandatory` Fragen, sodass das Interview hier zu Ende ist. Beide Events sind in `<anmeldung>-fragen.yml` definiert. Die `Testergebnisse` sind der Übersicht halber in der Datei `templates/Testmodus.md` ausgelagert und werden als `testergebnis`-Template in der `<anmeldung>.yml`-Datei geladen.

Für alle Fragen ist das `.util`-Modul importiert, welches einige nützliche Funktionen zum Auslesen der Konfiguration aus `<anmeldung>.yml` zur Verfügung stellt.

### Automatisches Abspeichern

Wird eine Definition der `Abschicken`-Variable gesucht, wird ein spezieller `code`-Block in der `data.yml`-Datei ausgelöst. Dieser startet mehrere Hintergrundaufgaben, die das Abspeichern übernehmen und aktiviert dann das `Warten`-Event (welches einen Wartebildschirm aus `<anmeldung>-fragen.yml` zeigt). Wird das Interview erneut ausgeführt (z.B. wenn ein `reload`-Event am Ende einer Hintergrundaufgabe eintritt), wird der `Abschicken`-Block erneut ausgeführt. Dies wird wiederholt, bis alle Hintergrundaufgaben beendet sind. Dann erst wird die `Abschicken`-Variable tatsächlich definiert und das Interview wird mit dem Schlussevent beendet.

Die einzelnen Hintergrundaufgaben sind in `tasks.yml` definiert. Diese delegieren allerdings im Wesentlichen an das `.ljo`-Modul. Dieses Modul übernimmt die tatsächliche Ausführung der API-Calls und ist selbst dokumentiert.

### Testmodus

Jede Hintergrundaufgabe in `tasks.yml` hat zwei Ausführungsmodi. Im normalen Modus wird die Hintergrundaktion ausgeführt. Im Testmodus wird die Aktion nicht ausgeführt. Stattdessen werden API-Calls gemacht, um zu prüfen, ob die Aktion normal ausgeführt werden kann. Es werden dann Variablen gesetzt, die die Ergebnisse dieser Tests enthalten. Im `testergebnis`-Template (in der `templates/Testmodus.md`) wird dann auf diese Variablen zugegriffen, um die Ergebnisse der Tests anzuzeigen. Dabei helfen einige Mako-`%def`s aus `defs.yml`.

Zuletzt kann jede Hintergrundaufgabe auch per JavaScript-API aufgerufen werden. Wird eine Aufgabe so direkt ausgeführt, wird sie auch im Testmodus ausgeführt. Auf diese Weise kann in den Testergebnissen eine “Trotzdem ausführen” Aktion angeboten werden.

Der Testmodus kann über die Konfiguration in `<anmeldung>.yml` oder über einen `test` URL-Parameter aktiviert werden.

## Konfiguration

Die automatischen Anmeldungen verwenden [Dienstkonten](https://cloud.google.com/iam/docs/service-accounts?hl=de) (Service Accounts), um sich mit der G Suite API zu authentifizieren. Das Dienstkonto hat die E-Mail `anmeldung@docassemble-264719.iam.gserviceaccount.com`. Der Service-Account ist im GCP-Projekt `docassemble-264719` konfiguriert und ist mit [domänenweiter Delegation](https://developers.google.com/admin-sdk/directory/v1/guides/delegation) autorisiert. Dies ist nötig, um Mitglieder zu Gruppen hinzuzufügen. Alle anderen Aktionen können im Namen des Service-Accounts ausgeführt werden, indem dem Account Schreibzugriff auf die nötigen Resourcen gegeben wird.

