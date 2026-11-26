# LEA BOS mobil für Home Assistant – Lesen

Version **0.3.0 - experimentelle Testversion**, entwickelt aus der bereitgestellten LEA-Android-Datei 2.0.0. Es handelt sich um eine inoffizielle Custom Integration.

Der Code ist erstellt und offline geprüft. Version 0.2.0 hat in einer HA-Instanz erfolgreiche, wiederholte Abrufe einer leeren persönlichen Inbox geliefert. **Ein echter neuer Alarm und die Tonwiedergabe von Version 0.3.0 auf Hardware sind noch nicht vollständig getestet.** Bei einer neuen persönlichen Anmeldung wurde eine automatische Abmeldung des anderen Geräts gemeldet. Ein verlässlicher Parallelzugang mit derselben persönlichen Sitzung ist nicht bestätigt. Die Integration ist eine ergänzende Anzeige; die LEA-App bleibt für die reguläre Alarmierung erforderlich.

## HA-Alarmierung mit originalen LEA-Tönen

Alle 39 Audiodateien aus `res/raw/` der bereitgestellten APK sind im Integrationsordner enthalten. Die beiden identischen Lautlos-Dateien werden als eine Option angeboten: **38 auswählbare Töne einschließlich Lautlos**. Dazu gehören FW Prio 1–3, RD Prio 1–3, FR Neu, KT, Alarm, Alarm 1–2, Martinshorn, Sirene, Gong, Ring, Glocken, Ding-Töne, Türklingeln und weitere kurze Benachrichtigungstöne. Ein separater Download oder Upload nach `/config/www` ist nicht erforderlich.

Unter **Einstellungen → Geräte & Dienste → LEA BOS mobil → Konfigurieren**:

1. Ein oder mehrere HA-Mediengeräte auswählen, die Audio-URLs wiedergeben können.
2. Alarmton, Lautstärke und maximale Wiedergabedauer auswählen.
3. Speichern und am LEA-Gerät die Taste **HA-Alarmton testen** verwenden.
4. Nach erfolgreichem Gerätetest die Option **Neue LEA-Alarme in HA mit Ton wiedergeben** aktivieren.

Die automatische Wiedergabe ist zunächst ausgeschaltet. Sie reagiert nur auf neu erkannte persönliche Meldungen mit Kategorie `alarm` (LEA-Typen 100/60). Informationen, Nachrichten und Stornos bleiben stumm. Ein Probealarm kann dieselbe Kategorie haben und dann ebenfalls auslösen. Vorhandene Meldungen beim ersten Einlesen werden nicht abgespielt; bereits bekannte Meldungs-IDs werden nach einem Neustart nicht erneut abgespielt.

Die Tonausgabe erfolgt im HA-Backend und funktioniert auch bei geschlossenem Dashboard. **HA-Alarmton stoppen** beendet die noch verwaltete Wiedergabe. Die Zeitoption begrenzt die Wiedergabe; kurze Töne werden nicht in einer Schleife wiederholt. Geräte und Netzwerk können Start und Stopp verzögern. Die vom Gerät gemeldete vorherige Lautstärke wird anschließend wiederhergestellt, sofern sie zwischenzeitlich nicht manuell geändert wurde. Geräte ohne Lautstärkerückmeldung erlauben diese Wiederherstellung nicht. Der aktuelle Medieninhalt wird nicht gesichert; auf den gewählten Geräten kann laufende Wiedergabe unterbrochen werden. Alexa-Geräte unterstützen nicht generell beliebige lokale Audiodateien und benötigen einen erfolgreichen Gerätetest.

In der LEA-Seitenleiste gibt es den Bereich **Alarmtöne** mit Browser-Vorschau aller Töne, aktuellem HA-Tonstatus und den Test-/Stopptasten für die gewählten HA-Geräte. Die Vorschau spielt auf dem Browsergerät. Auswahl und Aktivierung erfolgen in den Integrationsoptionen. Die HA-Basisadresse muss von den Wiedergabegeräten erreichbar sein.

Diese Einstellungen und Tasten ändern ausschließlich HA-Geräte. Sie verändern keine Töne, Lautstärken oder Alarmierungswege in der LEA-App und senden keine Quittierung an LEA. Herkunft und SHA-256-Werte stehen in [ATTRIBUTION.md](custom_components/lea_noe/frontend/ATTRIBUTION.md) und [catalog.json](custom_components/lea_noe/frontend/sounds/catalog.json).

### Bestehende Dashboardkarte aktualisieren

Wenn die Karte bisher als Inline-Ressource eingerichtet wurde, deren Ressourcen-URL nach dem Integrationsupdate durch `/lea-noe-static/lea-card.js?v=0.3.0` ersetzen und den Browser vollständig neu laden. Nur eine LEA-Kartenressource registrieren. Der automatisch angelegte Panel-Eintrag verwendet die mitgelieferte Version bereits selbst.

## Seitenleiste und Ansicht

Ab Version 0.2.0 wird nach erfolgreicher Einrichtung automatisch der Eintrag **LEA** in der HA-Seitenleiste angelegt. Die Ansicht zeigt persönliche Meldungen als Liste mit Suchfunktion und Detailansicht. Sie verwendet das originale LEA-Logo und die Farben der App. Es handelt sich um eine neu entwickelte, ausschließlich lesende HA-Oberfläche; sie bildet die App nicht vollständig nach.

Die Bereiche **Meldungen**, **Karte** und **Verbindung** dienen der Anzeige. Es gibt keine Zusage-, Absage- oder Quittierungsbedienung. Ein vorhandenes Dashboard unter dem Pfad `lea-noe` wird respektiert und nicht überschrieben. Die eigenständige Seitenleiste und die vollständige Listen-Schnittstelle sind auf HA-Administratoren beschränkt.

Die Kartenansicht benötigt gültige Einsatzkoordinaten und die aktivierte Detailoption der Integration. Eine externe OpenStreetMap-Karte wird erst nach einem bewussten Klick geladen; die Oberfläche nennt dabei die Übermittlung des Kartenausschnitts und der Einsatzkoordinaten. Ohne diesen Klick wird keine externe Karte eingebettet.

Die Ansicht liest den vorhandenen HA-Datenstand über eine authentifizierte, lesende WebSocket-Schnittstelle. Dadurch entstehen keine zusätzlichen LEA-Anmeldungen oder Quittierungen. Bestehende Karten auf Version 0.1.0 können zunächst die letzte Meldung darstellen; die vollständige Liste benötigt das Integrationsupdate.

Originalgrafiken: siehe [Herkunft und Kennzeichnung](custom_components/lea_noe/frontend/ATTRIBUTION.md).

## Installation mit HACS

[Repository direkt in HACS öffnen](https://my.home-assistant.io/redirect/hacs_repository/?owner=eignerth2010-byte&repository=ha-lea-noe&category=integration)

1. In Home Assistant **HACS** öffnen.
2. Über das Menü oben rechts **Benutzerdefinierte Repositories** öffnen.
3. `https://github.com/eignerth2010-byte/ha-lea-noe` als Repository eintragen und **Integration** als Typ auswählen.
4. **LEA BOS mobil (Lesen)** suchen, öffnen und herunterladen.
5. Home Assistant über seine Oberfläche neu starten.
6. **Einstellungen → Geräte & Dienste → Integration hinzufügen → LEA BOS mobil (Lesen)** öffnen.
7. **Vorhandener Sitzungstoken** oder **SMS-Anmeldung / Gerätewechsel (iPhone)** wählen. Ein neuer SMS-Login kann das andere LEA-Gerät abmelden. Die Anmeldung direkt in Home Assistant durchführen.

Das ist ein benutzerdefiniertes HACS-Repository; eine Aufnahme in die HACS-Standardliste ist dafür nicht erforderlich. Updates werden über dieses Repository bereitgestellt.

## Manuelle Installation

1. ZIP-Datei entpacken.
2. Den enthaltenen Ordner `custom_components/lea_noe` nach `/config/custom_components/lea_noe` auf dem Home-Assistant-System kopieren. `manifest.json` muss direkt in diesem Ordner liegen.
3. Home Assistant über seine Oberfläche neu starten.
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → LEA BOS mobil (Lesen)** öffnen.
5. Die gewünschte Anmeldung wählen. Bei einem **SMS-Gerätewechsel** die in LEA hinterlegte Handynummer eingeben und den SMS-Code anschließend direkt in Home Assistant eintragen. Die Nummer kann mit `+43`, `0043` oder österreichisch mit `0` beginnen. Ein neuer Login kann das andere Gerät abmelden.

Die Eingabe und Speicherung der Zugangsdaten erfolgt in deinem Home Assistant. Bitte keine SMS-Codes oder Sitzungstoken in einen Chat schreiben.

Alternativ gibt es **Vorhandener Sitzungstoken**. Das ist ein persönlicher LEA-Sitzungstoken, kein Infoscreen-Token. Dieser Weg führt ausschließlich Leseanfragen aus und fordert keine SMS an. Er setzt voraus, dass dir ein solcher eigener Token bereits zur Verfügung steht.

**Parallelbetrieb:** Bei erneuter persönlicher Anmeldung wurde eine automatische Abmeldung auf dem anderen Gerät beobachtet. Das Fälschen einer Gerätekennung ist keine bestätigte Lösung. Derselbe bestehende Sitzungstoken vermeidet technisch einen neuen Login, seine parallele Nutzung ist jedoch nicht serverseitig bestätigt. Es ist kein verifizierter normaler Token-Export aus der Smartphone-App beschrieben. Für einen vom persönlichen Login getrennten Betrieb ist ein vom Betreiber dafür bereitgestellter Lesezugang erforderlich; der Infoscreen-Zugang ist eine andere Zugangsart und wird von dieser persönlichen Integration nicht unterstützt.

## Welche Anmeldung ist implementiert?

Die App 2.0.0 lässt im iOS-Anmeldeweg einen leeren Push-Token zu. Genau diesen Ablauf verwendet die SMS-Anmeldung dieser Testversion. Der Android-Anmeldeweg verlangt im App-Code einen Push-Token und wird hier nicht nachgebildet. Die Integration registriert keinen eigenen Push-Empfänger.

Bei einer SMS-Anmeldung sind zwei Authentifizierungsanfragen nötig: SMS anfordern und Sitzung anlegen. **Die Anforderung „nur lesen“ gilt für den anschließenden Betrieb und alle Einsatzdaten.** Es gibt keine Quittierungs-, Lesebestätigungs-, Zusage-, Absage-, Status- oder Push-Token-Änderungsfunktion. Die Integration meldet die Sitzung auch beim Entfernen nicht beim LEA-Server ab.

Vor der produktiven Nutzung muss mit deinem Konto geprüft werden, ob die Anmeldung ohne Push-Token akzeptiert wird und die LEA-App auf deinem Handy weiterhin zuverlässig empfängt. Der App-Code enthält einen Hinweis bei Wechsel zwischen iOS und Android; deshalb den SMS-Anmeldeweg dieser Version nicht für einen Android-Hauptzugang verwenden.

## Entitäten

Die tatsächlichen Entitäts-IDs vergibt Home Assistant beim Hinzufügen; sie können umbenannt werden.

| Entität | Inhalt |
|---|---|
| Letzte Meldung | Kategorie der zuletzt abrufbaren persönlichen Meldung; Attribute mit ID, Einsatznummer, Art, Alarmstufe und Zeit |
| Meldungen im Abruffenster | Anzahl persönlicher Meldungen im aktuellen Abruf, maximal 100; keine Aussage über aktive Einsätze |
| Letzter erfolgreicher Abruf | UTC-Zeitpunkt des letzten vollständigen, erfolgreichen Abrufs |
| Neue Meldung (Event) | Ein Ereignis für jede neu erkannte persönliche Meldungs-ID |

Das Event verwendet folgende Typen aus der Zuordnung im App-Code:

| Eventtyp | LEA-Nachrichtenart-ID | Bedeutung |
|---|---|---|
| `alarm` | 100, 60 | Meldung/Alarmierung, einschließlich Probealarm, wenn LEA ihn so einordnet |
| `information` | 10 | Info-Meldung |
| `cancellation` | 30 | Storno |
| `message` | 20, 40 | Nachricht/Aktivität |
| `unknown` | andere oder fehlende ID | Keine belegte Zuordnung verfügbar |

Für Automationen kannst du die Event-Entität „Neue Meldung“ als Auslöser auswählen und nach dem Ereignistyp filtern. Alarmierung, Information und Storno sind getrennte Ereignistypen. Vorhandene Meldungen beim allerersten Start dienen als Ausgangsstand und lösen keine Alarme aus. Ein danach eintreffender Alarm erzeugt ein Ereignis, auch wenn vorher keine Meldung vorhanden war.

Die erkannten IDs werden lokal gespeichert. Nach Neustarts werden bereits bekannte IDs nicht erneut als neue Meldungen behandelt. Bei einer Änderung unter derselben Meldungs-ID entsteht kein neues Ereignis; eine neue ID zum selben Einsatz wird erkannt. Nach langen Ausfällen können Meldungen außerhalb des Abruffensters fehlen. Eine Änderung des Inhalts unter derselben ID ist im Sensor sichtbar, erzeugt aber kein neues Ereignis.

## Optionen

Unter **Einstellungen → Geräte & Dienste → LEA → Konfigurieren**:

- **Abrufintervall:** 30 bis 300 Sekunden, Standard 30. Der Empfang erfolgt durch Abfragen, nicht per Push. Serverbegrenzungen und Netzstörungen können die Verzögerung verlängern.
- **Meldungstext und Einsatzort anzeigen:** standardmäßig aus. Bei Aktivierung erscheinen `meldebild`, `nachricht`, `einsatzort` und gültige Koordinaten in den Attributen des Sensors "Letzte Meldung" sowie in der vollständigen Meldungsliste der Administratoransicht. Dadurch können diese Inhalte auch in HA-Verlauf und Backups gespeichert werden. Die Event-Entität enthält weiterhin ausschließlich die Grundattribute.

Die Integration fordert keine Patienten-Unterressourcen oder Rückmeldelisten an und übernimmt keine Patientenobjekte, Personennamen oder Teilnehmerlisten in Entitäten. Ein freier Meldungstext kann personenbezogene Angaben enthalten; die Detailoption ist deshalb bewusst ausgeschaltet. Konto- und Meldungsinhalte erscheinen nicht in der herunterladbaren Integrationsdiagnose.

## Abruf und Fehlerfälle

Es werden bis zu 100 persönliche Inbox-Einträge und ergänzend die jüngsten 25 Einsatzübersichten mit eingebetteten Meldungen geladen. Nur Meldungen aus der persönlichen Inbox erzeugen Entitäten/Ereignisse; zusätzliche Meldungen anderer Empfänger werden nicht als eigene Meldungen importiert. Wenn Kontext oder Typ nicht verfügbar sind, bleiben sie leer bzw. `unknown`.

- Ein abgelaufener Sitzungstoken löst die Home-Assistant-Neuanmeldung aus. Es gibt keine automatische neue SMS und keine erfundene Token-Erneuerungsschnittstelle.
- Bei Netzfehler, Zugriffsverweigerung oder unerwartetem Datenformat werden die Entitäten nicht verfügbar. Ein Fehler wird nicht als „keine Alarme“ ausgegeben.
- Eine vom Server gelieferte Wartezeit bei HTTP 429 wird berücksichtigt.
- Zeitstempel ohne Zeitzonenangabe bleiben unbekannt; die Integration rät keine Alarmzeit.
- HTTP-Weiterleitungen werden nicht verfolgt. Die Zieladresse ist im Client fest auf die HTTPS-LEA-API begrenzt.

## Entfernen

Die Integration unter Geräte & Dienste entfernen. Dadurch werden die lokalen Anmeldedaten und der zugehörige Erkennungsstand in Home Assistant entfernt. Es erfolgt keine Abmelde- oder Löschanfrage an LEA. Der kopierte Ordner kann anschließend über deinen üblichen Dateizugriff entfernt werden.

## Entwicklung und Prüfung

Benötigt wird Home Assistant **2026.11 oder neuer**; der Config-Flow verwendet dessen Schema-Bibliothek `probatio`. Die Kernlogik kann mit Python 3.12 ohne zusätzliche Pakete geprüft werden:

```text
python -m unittest discover -s tests -v
python -m compileall -q custom_components
python tests/validate_repository.py
```

Der Teststand und die noch offenen Live-Prüfungen stehen in [VALIDIERUNG.md](VALIDIERUNG.md). Die aus der Datei belegten Protokolldetails stehen in [PROTOKOLL.md](PROTOKOLL.md). Der Workflow **Offline tests** führt die Offline-Tests und die Paketprüfung bei Änderungen auf GitHub aus.

Das Repository enthält eigenen Integrationscode, Tests und Dokumentation sowie die auf Nutzerwunsch übernommenen originalen LEA-Grafiken mit Herkunftshinweis. APK-Dateien und fremder App-Programmcode werden nicht mitgeliefert.

Fehler können über [GitHub Issues](https://github.com/eignerth2010-byte/ha-lea-noe/issues) gemeldet werden. Bitte dabei die Integrationsversion, die Home-Assistant-Version und die Integrationsdiagnose angeben. Keine Handynummern, Sitzungstoken, SMS-Codes oder echten Einsatztexte veröffentlichen.

