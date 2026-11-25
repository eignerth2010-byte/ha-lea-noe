# Technischer Befund – LEA 2.0.0

Analysiert am 25.11.2026: `LEA+BOS+mobil_2.0.0_APKPure.xapk`, 32.345.669 Bytes, Paketname `at.notrufnoe.lea`, Versionscode `2000`.

SHA-256 der bereitgestellten XAPK:

```text
32f13e4d51b13c0800414ba28e2d0b30c1b057e2219a59e1ef190ae8163e1fa3
```

Die Datei wurde als ZIP gelesen und ihre JavaScript-Assets statisch untersucht. Sie wurde nicht ausgeführt. Dieser Hash identifiziert die untersuchte Datei; eine Prüfung ihrer Herstellersignatur wurde nicht durchgeführt.

## Im bereitgestellten App-Code belegt

Basis: `https://lea.api.notrufnoe.at`. Header: `Api-Version: 2`, `Authorization: Bearer <Sitzungstoken>` nach Anmeldung sowie `X-User-Agent`. Der Custom Client identifiziert sich im User-Agent als Home-Assistant-Leseclient.

| Methode/Pfad | Felder bzw. Ergebnis | Verwendung |
|---|---|---|
| POST `/devices` | `telefonnummer`, `platform`, `pushNotificationToken`; Antwort mit `message`/`Nachricht` oder `token` | Nur nach ausdrücklicher SMS-Anforderung im Konfigurationsdialog |
| POST `/sessions` | `telefonnummer`, `smsToken`, `pushNotificationToken`, `platform`; Antwort mit `token` und `user` | Nur Anmeldung im Konfigurationsdialog |
| GET `/me` | Profil einschließlich `id` | Kontoprüfung und stabile Kontozuordnung |
| GET `/notifications` | `items`, im App-Code mit `limit: 100` aufgerufen | Persönliche Meldungen |
| GET `/incidents` | `items`, Parameter `limit`, `offset`, optional `with` | Ergänzende Einsatzdaten; keine Rückmeldelisten angefordert |

Die Laufzeitfreigabe im Client umfasst genau die drei genannten GET-Pfade. Authentifizierungs-POSTs sind nur für getrennt erzeugte Konfigurationsclients aktiviert. Der Client bietet keine anderen Schreiboperationen.

Quellen innerhalb des bereitgestellten Pakets:

| Asset | Befund |
|---|---|
| `assets/public/chunk-BRkWAvZ4.js` | Produktionshost, API-Version, Bearer-Header, HTTP-Client |
| `assets/public/chunk-C9wsXYYE2.js` | Registrierung, SMS-Sitzung, Push-Token-Prüfung; leerer Push-Token ausschließlich im iOS-Anmeldeweg im Client zugelassen |
| `assets/public/chunk-CHdsMqar2.js` | SMS-Eingabe und Hinweis bei Plattformwechsel |
| `assets/public/chunk-BBKhSYCo2.js` | Persönliche Inbox, Einsatzliste, DTO-Felder, optionale Unterressourcen |
| `assets/public/chunk-DRofqRBM.js` | Zuordnung Nachrichtenart-IDs zu Kategorien |
| `assets/public/chunk-Lqg5tKWv2.js` | Profilstruktur mit `id`, Namen, Organisationen und Telefonnummern |

Die Integration übernimmt nicht die nach Anmeldung im App-Code zusätzlich ausgeführten Vorgänge zur Push-Token-Synchronisierung, Geräte-Schlüsselregistrierung oder Empfangsbestätigung. Deshalb ist das Verhalten eines eigenen Clients noch mit dem tatsächlichen Server zu prüfen.

## Öffentlich dokumentiert

- [LEA-Anleitung: Anmeldung mit Telefonnummer und fünfstelligem SMS-Code](https://wiki.feuerwehr.gv.at/lea/anleitung-fuer-installation-und-einrichtung-von-lea-188383398.html)
- [LEA-Projekthomepage](https://lea-app.at/)
- [Home Assistant: Config Flow](https://contributors.home-assistant.io/core/integrations/config-flow/)
- [Home Assistant: Datenabruf und Coordinator](https://contributors.home-assistant.io/core/integrations/fetching-data/)
- [Home Assistant: Event-Entitäten](https://contributors.home-assistant.io/core/entities/event/)
- [Home Assistant 2026.11.3: Config-Flow mit probatio](https://github.com/home-assistant/core/blob/2026.11.3/homeassistant/components/bluemaestro/config_flow.py)

Diese Unterlagen sind keine öffentliche Freigabe oder API-Dokumentation für diesen Custom Client. Die konkreten API-Abläufe oben stammen aus der bereitgestellten Datei.

## Noch nicht belegt

Keine echte Anmeldung, keine Live-Antwortstruktur des persönlichen Kontos, kein Empfangstest mit parallelem Handy, kein Lauf in einer Home-Assistant-Instanz. Insbesondere sind Serverakzeptanz der SMS-Anmeldung ohne Push-Token, Sitzungslaufzeit, Parallelbetrieb sowie Nebenwirkungen serverseitiger GET-Endpunkte ohne Live-Prüfung nicht zugesichert. Die Tests belegen die vom Client gesendeten Methoden, nicht das interne Verhalten des LEA-Servers.

