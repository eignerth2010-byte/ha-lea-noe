# LEA-Grafiken und Audiodateien

`lea-logo.svg` ist das unveränderte weiße LEA-Logo aus der vom Nutzer bereitgestellten LEA-App 2.0.0. Dieselben unveränderten SVG-Daten sind als Bild in `lea-card.js` eingebettet, damit die Karte auch ohne weitere externe Ressourcen funktioniert.

`../brand/icon.png` ist die unveränderte Grafik `assets/public/assets/logo_full.png` aus demselben Paket.

Logo und Kennzeichen gehören ihren jeweiligen Rechteinhabern, insbesondere Notruf Niederösterreich. Sie kennzeichnen den angebundenen Dienst. Diese Home-Assistant-Integration ist ein inoffizielles Projekt und wird nicht als offizielle LEA-App ausgegeben.

Layout und JavaScript dieser Oberfläche wurden für die ausschließlich lesende HA-Ansicht neu erstellt. Der mobile LEA-Programmcode und dessen fremde Bibliotheken werden nicht mitgeliefert.

Die Dateien unter `sounds/` stammen unverändert aus `res/raw/` der vom Nutzer bereitgestellten Datei `LEA+BOS+mobil_2.0.0_APKPure.xapk`, darin `at.notrufnoe.lea.apk`. Ihr ursprünglicher Dateiname, ihre Größe beziehungsweise Dauer und SHA-256-Werte sind im mitgelieferten `catalog.json` dokumentiert. `lautlos.mp3` und `silence.mp3` sind bytegleich und ergeben eine gemeinsame Auswahloption. Die separate Datei `assets/public/assets/tts.mp3` ist kein auswählbarer Alarmton und wird nicht mitgeliefert.

Die Grafiken und Audiodateien sind Originalmaterial ihrer jeweiligen Rechteinhaber. Eigener Integrationscode begründet keine Rechte an diesen Assets. Die Integration ist weiterhin inoffiziell. Die Wiedergabe steuert ausschließlich lokale HA-Mediengeräte; sie registriert keine eigenen LEA-Push-Geräte.
