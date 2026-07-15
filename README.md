# DistributedSystemsProject

Diese Zusammenfassung wurde partiell mithilfe von Microsfoft Copilot verfasst. Sie beinhaltet eine Projektübersicht, den grundlegenden Datenfluss mit der oberflächlichen Beschreibung der einzelnen Komponenten sowie allgemeine Installations- und Run-Hinweise.

## 1. Allgemeines

### 1.1 Übersicht 
Dieses Robotik‑Telemetrie‑System besteht aus:
- Python‑MQTT‑Publishern (Positions‑ & Geschwindigkeitsdaten)  
- zusätzlich Python-Subscriber zum Debuggen
- Java Spring Boot‑Backend (MQTT‑Subscriber, REST‑API, Datenpufferung)  
- Web‑Dashboard (HTML/CSS/JS + Chart.js für Live‑Tracking)  

Das Projekt demonstriert die Integration von Messaging, Backend‑Verarbeitung und Echtzeit‑Visualisierung in einem verteilten System.

### 1.2 Ziel
Dieses Projekt dient als Demonstration für:
- verteilte Systeme
- Messaging‑basierte Kommunikation
- Echtzeit‑Datenverarbeitung
- Web‑Visualisierung
- Integration von Python, MQTT und Java Spring Boot sowie Web-Technologien

Es eignet sich als Grundlage für Robotik‑Monitoring, Telemetrie‑Systeme oder verteilte Steuerungsarchitekturen.  
Die Projektstruktur wird künftig erweitert (z. B. Logging, Multi‑Joint‑Charts, Robot‑Arm‑Visualisierung).

### 1.3 Lizent/ Hinweise
FavIcon für das Dashboard:
- Favicon: Robot Icon by Icons8 (CC BY 4.0)


### 1.4 Projektstruktur
Die Projektstruktur sieht zum aktuellen Stand (Juli 2026) wie folgt aus:

    PLATZHALTER: STRUKTUR WIRD NOCH ERWEITERT

```bash
DistributedSystemsProject/
│
├── mqtt/                     # Python MQTT Publisher & Subscriber
│   ├── pos_publisher.py      # Publiziert Positionsdaten
│   ├── vel_publisher.py      # Publiziert Geschwindigkeitsdaten
│   ├── pos_subscriber.py     # Debug-Subscriber
│   ├── vel_subscriber.py     # Debug-Subscriber
│   └── utils.py              # Hilfsfunktionen
│
└── springboot/               # Java Spring Boot Backend + Dashboard
    ├── src/main/java/com/mende/examination/soarms/
    │   ├── ExaminationApplication.java   # Spring Boot Entry Point
    │   ├── MqttRobotSubscriber.java      # MQTT Subscriber (Robotikdaten)
    │   ├── RobotState.java               # Datenmodell
    │   ├── RobotStateService.java        # Speicherung & Historie
    │   └── RobotStateController.java     # REST API
    │
    ├── src/main/resources/static/
    │   ├── dashboard.html                # Web-Dashboard
    │   ├── css/dashboard.css             # Stylesheet
    │   └── js/dashboard.js               # Chart.js + Live-Update
    │
    └── pom.xml                           # Maven-Konfiguration
```

### 1.5 Abhängigkeiten
Es sind diverse Abängigkeiten hinzuzufügen, die sich auf mehrere Ebenen verteilen:
- Python: Paho-MQTT-Client (beinhaltet Bibliothek), installierbar mit pip install paho-mqtt==2.1.0
- Ubuntu-Pakete:
    - Maven (Java-Build-Tool), installierbar mit sudo apt install maven
    - Mosquitto (MQTT-Broker), installierbar mit sudo apt install mosquitto
- VSCode-Extensions zur Entwicklung:
    - Spring Boot Dashboard
    - Spring Boot Extension Pack
    - Spring Boot Tools
    - Spring Initializr Java Setup



## 2. Pythonseitiger MQTT‑Datenfluss
Die Python‑Skripte simulieren Robotertelemetrie und senden periodisch:
- Positionsdaten → Topic `leader/pos`
- Geschwindigkeitsdaten → Topic `leader/vels`

Wichtig ist, dass die Arbeitsumgebung die in 1.5 aufgelisteten Anforderungen erfüllt. Ist dies der Fall, kann mit diesem Code in den Zielordner gewechselt werden:
```bash
cd <path_to_the_repo>
cd mqtt
```
Aus diesem Ordner können die Publisher gestartet werden:
```bash
python3 pos_publisher.py
python3 vel_publisher.py
```
Zum Debugging können auch die Python-Subscriber verwendet werden.



## 3. Javasetiger Datenfluss
### 3.1 Java-Subscriber und -Service
Der Java‑Subscriber empfängt die Daten über Eclipse Paho und schreibt sie in den `RobotStateService`.  
Der Service:
- speichert den aktuellen Zustand
- führt eine Positionshistorie (trägt dort gesamplete Werte ein, löscht älteste Werte, wenn Pufferlimit erreicht)
Dabei enthält der Zustand Informationen über aktuelle Geschwindigkeiten und Positionen der Gelenke sowie den Zustand des Systems.

### 3.2 REST‑API (Spring Boot)
Die REST-API dient zum HTTP-Aufruf der Zustandsdaten. Diese sind im json-Format und können so im Browser angezeigt werden.
Endpoint	Beschreibung
`GET /api/robot/state`	    liefert aktuellen Maschinenzustand, Positionen, Geschwindigkeiten
`GET /api/robot/posList`	lefert die Positionshistorie für Live‑Charts

Beispiel‑Response:
```json
{
  "machineState": "RUNNING",
  "pos": [12.3, 5.1, -3.0, 0.0, 1.2, 0.8],
  "vels": [0.1, 0.0, -0.2, 0.0, 0.0, 0.1]
}
```

### 3.3 Web‑Dashboard
Das Dashboard zeigt:
- `pos` (aktueller Gelenkwinkel)
- `vels` (aktuelle Gelenkgeschwindigkeit)
- `machineState` (aktuellen Zustand des Roboters)
- Live‑Tracking‑Chart (Chart.js) mit Buttons zum Umschalten der Gelenke (Joint 0–5)

Es verfügt über die folgenden Technologien:
- HTML5
- CSS3 (Flexbox‑Layout)
- JavaScript (Fetch API, Chart.js)
- REST‑API‑Integration
- Live‑Update alle 400 ms




## 4. Projekt starten
1. Ein Terminal öffnen, dort in den `springboot`-Ordner des Repos wechseln und `mvn spring-boot:run` eingeben.

2. Öffne einen Browser. Die REST-Endpoints sind nun unter `localhost:8080/api/robot/state` und `localhost:8080/api/robot/posList` erreichbar, die json-Daten sind einsehbar. Des Weiteren kann mit `localhost:8080/dashboard.html` das Dashboard angezeigtt werden. Es dürften noch keine Positionen, Geschwindigkeiten oder Zustände angeziegt werden.

3. Öffne ein zweites Terminal, um den Python‑Publisher zu starten. Navigiere dafür in das `mqtt`-Verzeichnis des Repos, wechsle wenn nötig in die enstprechende Python-Umgebung und gib das ein:
```bash
python3 pos_publisher.py
```
oder
```bash
python3 vel_publisher.py
```
Jetzt muss sich das Dashboard live aktualisieren und beim Erneuten Abrufen der REST-Endpoints über GET-Methoden (entweder mit curl oder im Browser) werden die aktuellen Daten angezeigt.