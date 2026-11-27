# Ergänzung Version 0.4.0 – 27.11.2026

41 Offline-Tests erfolgreich; Paketprüfung und JavaScript-Syntaxprüfung erfolgreich. Geprüft sind persönliche Gruppen aus dem Profil, keine Übernahme fremder Mitgliedschaften, keine Personen-/Telefonfelder, ID-Zuordnung ausschließlich an der eigenen Meldung, Profil-Cache und Fortsetzung des Meldungsabrufs bei ausgefallenem optionalem Gruppenabruf. Fehlende Gruppenfelder sind kein bestätigter leerer Gruppenstand. Der Live-Gruppenabruf von 0.4.0 und ein echter Probealarm sind zum Veröffentlichungszeitpunkt noch nicht verifiziert.

# Prüfstand – Version 0.3.0

Stand: 26.11.2026. Zielsystem: Home Assistant 2026.11.3; Mindestversion dieser Implementierung: 2026.11.

## Ausgeführt

**32 Offline-Tests bestanden** mit `python -m unittest discover -s tests -v` unter Python 3.12. Keine Verbindung zu einem echten LEA-Konto wurde dabei aufgebaut. Zusätzlich werden die Begrenzung und die optionale Freigabe der Einsatzkoordinaten geprüft.

Geprüft werden:

- Keine Authentifizierungs- oder Einsatzschreibanfragen durch den Laufzeitclient; ausschließlich drei feste GET-Endpunkte.
- Freigabe der zwei Authentifizierungs-POSTs ausschließlich bei explizit aktiviertem Anmeldeclient; andere Schreibpfade bleiben gesperrt.
- SMS- und Login-Payload entsprechend dem iOS-Anmeldeweg im bereitgestellten App-Code.
- Persönliche Inbox als Auswahlgrundlage; zusätzliche eingebettete Meldungen anderer Empfänger werden nicht importiert.
- Doppelte Meldungs-IDs, Start mit vorhandenen Meldungen, Start mit leerer Inbox, Neustart, neue Meldungs-IDs zum selben Einsatz und begrenzte lokale ID-Speicherung.
- Ausblendung von Detailtext und Einsatzort als Standard; keine Übernahme von Patientenobjekten in das Datenmodell.
- Trennung von Authentifizierungsfehlern, Zugriffsfehlern, Serverfehlern und Begrenzung der Abrufrate.
- Weiterleitungen, ungültiges JSON, fehlende/störende Listenstrukturen, zu große Antworten, fehlende Sitzungstoken und fehlende stabile Meldungs-ID.
- Fehlertexte und Client-Darstellung ohne Sitzungstoken oder ungefilterte Serverinhalte.
- Telefonnummern-Normalisierung, bekannte Kategorien und Zeitstempel; unbekannte Informationen werden nicht aus der Einsatzübersicht geraten.

Zusätzlich erfolgreich: Python-Syntaxprüfung aller Integrationsdateien und JSON-Prüfung von Manifest sowie englischen/deutschen Übersetzungen. Die Config-Flow-Schemabibliothek und die verwendete Event-Entity-Schnittstelle wurden mit dem Quellcode von Home Assistant 2026.11.3 verglichen.

## Grenzen dieser Prüfung

Die HTTP-Antworten in den Tests sind synthetische Beispiele auf Basis der aus dem App-Code belegten Feldnamen. Sie stammen nicht aus einem echten Konto. Die Tests laden die echte API-, Modell- und Erkennungslogik, jedoch nicht die HA-Integration in einer laufenden HA-Instanz. Config-Flow, Coordinator, Entitäten und Optionsdialog sind daher nicht durch einen HA-Laufzeittest bestätigt.

Noch offen sind insbesondere:

1. Annahme des erkennbar als Home-Assistant-Client auftretenden HTTP-Clients durch LEA.
2. Echte SMS-Anmeldung ohne Push-Token und Akzeptanz der persönlichen Sitzung.
3. Genaue Antwortstruktur und Berechtigungen des tatsächlichen Kontos.
4. Fortbestehender Empfang und unveränderte Kontokonfiguration in der parallel genutzten Handy-App.
5. Einrichtung, Neuanmeldung, Optionen und neue Event-Entität in Home Assistant.
6. Verhalten bei einem tatsächlichen neuen Alarm sowie einem Storno.
7. Mögliche interne Nebenwirkungen der GET-Endpunkte auf dem Server. Der Client selbst sendet keine Empfangs- oder Lesebestätigung.

Die Version ist deshalb ausdrücklich **experimentell und noch nicht produktiv verifiziert**. Nach der ersten Bereitstellung wurde eine automatische Abmeldung des anderen LEA-Geräts bei einer neuen persönlichen Anmeldung gemeldet. Die Konfiguration kennzeichnet den SMS-Weg deshalb als möglichen Gerätewechsel und verlangt eine bewusste Bestätigung. Die Wiederverwendung eines persönlichen Tokens ist als Parallelzugang nicht verifiziert.

Die LEA-Dashboardkarte wurde in der vorhandenen HA-Instanz mit dem originalen Logo und der Seitenleistenverknüpfung sichtbar geprüft. Zum Prüfzeitpunkt lieferten die LEA-Sensoren keinen aktuellen Datenstand. Eine Prüfung mit echten Meldungen, einer mobilen Browserbreite und gültigen Einsatzkoordinaten steht noch aus. Ein bestehendes Dashboard unter `lea-noe` wird vom neuen automatischen Panel nicht überschrieben.


## HA-Tonwiedergabe in 0.3.0

Die zusätzlichen Tests verwenden einen simulierten HA-Servicebus und prüfen: automatische Wiedergabe nur bei freigegebener Alarmkategorie, expliziter Test bei ausgeschalteter Automatik, verfügbare und ausgefallene Geräte, unveränderte Lautstärke nach einem Stopp, Erhalt manueller Änderungen und das Verhindern von Wiedergabe nach dem Entladen. Die 38 Katalogoptionen werden gegen die unveränderten enthaltenen Audiodateien und deren SHA-256 geprüft. Die Paketprüfung umfasst alle 39 Audioassets.

Der HA-Datenabruf mit Version 0.2.0 wurde am 26.11.2026 erfolgreich beobachtet; die persönliche Inbox war leer. Die neue Wiedergabesteuerung, Test-/Stopptasten und Optionen sind damit nicht als Hardwaretest bestätigt. Noch erforderlich sind Wiedergabe und Stopp auf den gewünschten Geräten, Erreichbarkeit der HA-Audio-URLs und ein tatsächliches neues Alarmereignis. Es wurde kein künstlicher LEA-Alarm erzeugt.
