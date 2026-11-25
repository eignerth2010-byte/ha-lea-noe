# Prüfstand – Version 0.1.0

Stand: 25.11.2026. Zielsystem: Home Assistant 2026.11.3; Mindestversion dieser Implementierung: 2026.11.

## Ausgeführt

**20 Offline-Tests bestanden** mit `python -m unittest discover -s tests -v` unter Python 3.12. Laufzeit beim ersten vollständigen Testlauf: rund 0,25 Sekunden. Keine Verbindung zu einem echten LEA-Konto wurde dabei aufgebaut.

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

Die Version ist deshalb ausdrücklich **experimentell und noch nicht produktiv verifiziert**. Die Analyse- und Testschritte rechtfertigen keine Aussage, dass die Anmeldung bereits funktioniert oder die reguläre Alarmierung unverändert bleibt.

