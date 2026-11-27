# Änderungen

## 0.4.0 – 27.11.2026

- Persönliche Alarmgruppen aus dem LEA-Profil, ausschließlich lesend und zwischengespeichert.
- Gruppenansicht in der Seitenleiste und Sensor mit Gruppenliste.
- Gruppen-ID und aufgelöster Name an persönlichen Meldungen und Ereignissen; keine Ableitung aus anderen Empfängern.
- Fehlerhafter Gruppenabruf lässt lesbare Meldungen weiter zu; Authentifizierungsfehler und Rate-Limits werden weitergereicht.
- 41 Offline-Tests, einschließlich Mitgliedschaftsbegrenzung und Gruppen-Zuordnung.


## 0.3.0 - 26.11.2026

- 39 unveränderte Audioassets aus der bereitgestellten LEA-APK direkt im Integrationspaket, 38 logische Tonoptionen einschließlich Lautlos.
- Lokale HA-Alarmierung mit Mediengeräteauswahl, Lautstärke und begrenzter Wiedergabe; automatische Wiedergabe standardmäßig aus.
- Eigenständige Test-/Stopptasten und Tonvorschau im neuen Seitenleistenbereich Alarmtöne.
- Neue persönliche Alarme lösen die Wiedergabe im HA-Backend aus, ohne ein geöffnetes Dashboard und ohne LEA-Schreibzugriff.
- Gerätefehler werden getrennt behandelt; ein ausgefallenes Gerät verhindert die Wiedergabe auf anderen gewählten Geräten nicht.
- Wiederherstellung gemeldeter Lautstärke unter Beachtung manueller Änderungen; laufende andere Medien werden beim Stoppen nach Möglichkeit erkannt.
- 32 Offline-Tests für Protokoll, neue Meldungen, Katalog und Wiedergabesteuerung. Hardware-Wiedergabe bleibt zu prüfen.

## 0.2.0 – 25.11.2026

- LEA-Seitenleisteneintrag für neue Installationen nach erfolgreicher Einrichtung.
- Meldungsliste, Suche, Detailanzeige und Verbindungsstatus im Stil der LEA-App.
- Originales LEA-Logo und App-Symbol mit Herkunftshinweis.
- Kartenansicht mit validierten Koordinaten, optionaler Detailfreigabe und bewusstem Laden von OpenStreetMap.
- Lesende, authentifizierte HA-Schnittstelle für vorhandene Meldungsdaten; vollständige Liste nur für HA-Administratoren.
- Unterstützung vorhandener 0.1.0-Sensoren als Ansicht der letzten Meldung.
- SMS-Anmeldung als möglicher Gerätewechsel gekennzeichnet; Bestätigung vor der SMS-Anforderung. Ein vorhandener Sitzungstoken wird im Anmeldemenü zuerst angeboten.
- 22 Offline-Tests sowie Paket- und JavaScript-Syntaxprüfung.

## 0.1.0

- Persönliche Anmeldung per SMS oder vorhandenem Token.
- Ausschließlich lesender Betrieb, Sensoren, Event-Entität und lokale Erkennung neuer Meldungs-IDs.
- Erstes benutzerdefiniertes HACS-Repository.
