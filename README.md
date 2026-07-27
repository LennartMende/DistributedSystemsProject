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

-> Somit kann das gesamte MVC-Konzept mit JS, CSS und HTML abgedeckt werden, wobei sich nur an Daten aus der RESTful API bedient wird. JS stellt somit zusammen mit der REST API den Übergang zwischen dem Backend und dem Frontend dar.

## Alarm
Da die Temperaturen und Spannungen der Motoren ausschlaggebende Indikatoren für den Zustand eines Motors sind, wurden Schwellwerte sowohl für die Temperatur als auch für die Spannung eingeführt. Dafür wurde ein Betrieb über 30 min durchgeführt. Af die gemessenen Temperaturwerte wurden 5 °C als Aufschlag für einen Warnhinweis gegeben und 7 °C als Aufschlag für eine kritische Meldung. Ebenfalls beim Unterschreiten um X °C. Da die Spannungn konstant um die Nennwerte bleiben und maximal um +/- 0,1 V schwanken, wurden +/- 5 % als Grenzwerte definiert, also ab 5,3 bzw. unter 4,8 V und unter 11,4 und über 12,6 V.  
Der Alarm ist innerhalb des JavaScript-Layers implementiert, da somit keine zusätzlichen Daten gepublisht oder subscribet werden müssen, letztendlich muss nur die Verarbeitungslogik auf Basis der von der RESTful API gewonnen (gegetteten) Daten gewonnen. 


## Historie der Daten
Da die Positionsdaten der beiden Roboterarme ausschlaggebend für die Regelung sind (Regel- und Führungsgröße) und gleichzeitig eine deutlich schnellere Dynamik aufweisen als Temperatur und Spannung, wird nur die Historie der Positionen aufgezeichnet. Zudem sin Spannung und Temperatur des Follower-Arms im Normalfall auch höher als auf dem Leader-Arm, was einen Vergleich zusätzlich erschweren würde.  
Die Leader- und Follower-Positionsdaten werden in `ArrayLists` gespeichert. Für das Anfhängen neuer Listenelemente gilt O(1). Außerdem kann Elementzugriff über den Index mit O(1) erfolgen, was für das Plotten hilfreich ist. Lediglich beim Löschen des ältesten Elements wäre die `LinkedList` mit O(1) effizienter.  
Damit die Operationen möglichst hardwareunabhängig in Echtzeit (die Echtzeitfür die UI wird durch die Aktualisierungsrate des Dashboards vorgegeben) erfolgen können, wird ein Sampling der Werte durchgeführt. Dabei wird nur ein von `sampleRate` Messpunkten gespeichert. Um den RAM nicht zu sehr zu belasten, werden außerdem nur die letzten `buffferCapacity` Messpunkte in der Historie gespeichert. Somit kann mit:  
bufferCapacity * sampleRate / fps
berechnet werden, die wie vielen letzten Sekunden aufgenommen werden. Dabei entspricht fps der Abtastrate der Sensorik in 1/s. Wenn der Aufbau bspw. nicht nur zur Live-Daten-Visualisierung, sondern auch zum Training eines maschinellen Lernmodells verwendet werden soll, kann auch die Samplingrate auf 1 gesteigert werden, damit keine Daten verloren gehen.

## Erweitertetes Datenformat für Metadaten -> Zeitstempel und Client-Identifikation
Zum Datenaustausch zwischen Python-Publishern, Java-Subscribern und der RESTful-API wird das json-Format verwendet, da es deskriptive Schlüssel ermöglicht. Es ist außerdem ein moderner Industriestandard und es gibt Python- und Java-Bibliotheken zum Parsen von json-Daten.  
Am Anfang des Projekts war der Payload der MQTT-Daten auf die physikalischen Größen reduziert, d. h. ein Python-Publisher hat bspw. das folgende Payload gepublisht:

```python
{"shoulder_pan": 0.0, "shoulder_lift": 0.0, "elbow_flex": 0.0, "wrist_flex": 0,0, "wrist_roll": 0.0, "gripper": 0.0}
```

Um zusätzlich Metadaten aufzuzeichnen, wurde dann das folgende Format eingeführt: 

```python
{"processTimeStamp" : float, "deviceId" : str, "data": s.o.}
```
Der `processTimeStamp` ist dabei eine Zeit in Sekunden, die seit dem Systemstart vergangen ist. `deviceId` bezeichnet jedes physikalische Objekt, für das Daten gepublisht werden können. `data` ist wie oben ein String, nur das jetzt zusätzlich die Keys die Endungen `.pos`, `.volt` und `.temp` tragen, um die zugehörige physikalische Größe darzustellen. Somit wird neben der Identifizierung der zugehörigen Maschine auch das Plotten entlang der x-Achse erleichert. Es mussten lediglich die Struktur des Python-MQTT-Publishers verändert werden. Zudem musste im Java-Subscriber ein neues Parsing für die `processTimeStamp` und die `deviceId` eingeführt und das Parsen der physikalischen Größe um eine Ebene tiefer verlegt werden.

## Docker-Setup für Mosquitto
bei Mosquitto-Installation über apt wird ein System-Daemon installiert. Standardmäßig startet dieser mit dem System und läuft im Hintergrund. Der Status kann mit 

```bash
systemctl status mosquitto
```

überprüft werden. Der Daemon kann mit
```bash
sudo systemctl stop mosquitto
```

Zur Verwendung des Docker-Mosquittos muss Port 1883 freigegeben werden. Dafür gibt man:
```bash
sudo systemctl disable mosquitto
```
in der Command Line ein. Damit startet Mosquitto nicht automatisch beim Boot-Vorgang.  
Anschließend wechselt man mit in den `mosquitto`-Ordner im Repo, da dieser die `docker-compose.yaml` enthält, die die Instruktionsanweisungen für den folgenden Befehl beinhaltet. Mit dem Befehl
```bash
docker compose up -d
```
kann nun die Docker-Anwendung gestartet werden. Die Wirkung kann anschließend überprüft werden, indem einer dieser 3 Befehle verwendet wird:

```bash
ss -tulpn | grep 1883 # bzw. 8883 für TLS, systemd-mosquitto muss beendet sein 
docker ps # zeigt Status der laufenden COntainer, bspw. eclipse-mosquitto:2
docker inspect -f '{{.State.Status}}' mosquitto # Status des Docker-Mosquittos
```
Nach der Session kann der Container (und somit der Mosquitto-Server) beendet werden:
```bash
docker compose down
```
Kurzbeschreibung, wie/ wieso yaml so funktioniert und was die Vorteile sind.

## Zertifikate
-> Warum Zertifikate?
-> Wer besitzt welche zertifikate?
-> Wie habe ich die Zertifikate erstelle? In welchem Ordner liegen die Zertifikate?
-> Port-Änderung: 1883 -> 8883
-> Wer erstellt die Zertifikate bzw. wer verwaltet und verteilt diese?
-> Was muss dafür in Java und Python geändert werden?

Die Zertifikate wurden so erstellt:
1. für Client: client_java_subscriber:
openssl genrsa -out client_java_subscriber.key 2048
 1869  openssl req -new     -key client_java_subscriber.key     -out client_java_subscriber.csr     -subj "/CN=java_subscriber"
 1870  openssl x509 -req     -in client_java_subscriber.csr     -CA ca.crt     -CAkey ca.key     -CAcreateserial     -out client_java_subscriber.crt     -days 365     -sha256
 1871  openssl pkcs12 -export     -inkey client_java_subscriber.key     -in client_java_subscriber.crt     -certfile ca.crt     -out client_java_subscriber.p12     -password pass:123456
 1872  keytool -importcert     -alias myca     -file ca.crt     -keystore truststore.p12     -storetype PKCS12     -storepass 123456     -noprompt
 1873  ss -tulpn | grep 8883
2. für server:
lennart@lennart-ubuntu:~/2.Semester/VerteilteSysteme/DistributedSystemsProject/mosquitto/certs$ openssl genrsa -out server.key 2048
lennart@lennart-ubuntu:~/2.Semester/VerteilteSysteme/DistributedSystemsProject/mosquitto/certs$ openssl req \
-new \
-key server.key \
-out server.csr \
-subj "/CN=localhost"
lennart@lennart-ubuntu:~/2.Semester/VerteilteSysteme/DistributedSystemsProject/mosquitto/certs$ openssl x509 -req \
-in server.csr \
-CA ca.crt \
-CAkey ca.key \
-CAcreateserial \
-out server.crt \
-days 365 \
-sha256
Certificate request self-signature ok
subject=CN = localhost
lennart@lennart-ubuntu:~/2.Semester/VerteilteSysteme/DistributedSystemsProject/mosquitto/certs$ openssl x509 -in server.crt -issuer -subject -noout
issuer=C = DE, ST = Saxony, L = Leipzig, O = HTWK, OU = HTWK-Robos, CN = Mende, emailAddress = lennart.mende@stud.htwk-leipzig.de
subject=CN = localhost

san.cnf:
openssl req -new -nodes -x509   -days 365   -keyout server.key   -out server.crt   -config san.cnf
-> Was macht man damit/ Was bringt der Befehl?

-> Was sind Keystore und Truststore?

Die Zertifikate für die Python-Clients können mithilfe des Shell-SKripts `create_certs.sh` generiert werden. Dabei wird über die beiden Arme `arm`, die physikalische Größe `quantity` und die Art des MQTT-Clients `client` iteriert. Somit kann für jeden Client ein angepasstes Zertifikat erzeugt werden. Für die Erzeugung an sich werden dann drei Schritte durchlaufen:
1. Befehl:
```bash
openssl genrsa -out "${NAME}.key" 4096
```  
2. Befehl:  
```bash
openssl req \
                -new \
                -key "${NAME}.key" \
                -out "${NAME}.csr" \
                -config client.conf \
                -subj "/CN=${arm}_${quantity}_${client}"
```  
3. Befehl:  
```bash
openssl x509 \
                -req \
                -in "${NAME}.csr" \
                -CA ca.crt \
                -CAkey ca.key \
                -CAcreateserial \
                -out "${NAME}.crt" \
                -days 3650 \
                -sha256
```  
Ausführung:
 1939  cd ../certs/
 1940  chmod +x create_certs.sh
 1941  ./create_certs.sh
 -> Erst in certs-Ordner wechseln, dann das Shell-Skript ausführbar machen und anschließend ausführen.
...
Da sie mit root/ lennart/ user auf dem Host erstellt wurden, hat der Mosquitto-Docker keinen Zugriff (Permission denied), da er als user mosquitto ist. Daher muss erst in der Ordner `DistributedSystemsProject/mosquitto/certs` gewechselt werden. Dort wird 


## Weiterhin grundsätzliche Fragen
### Was macht Maven?
### Was ist Springboots Zuständigkeit?
### Wie wird tomcat automatisch gestartet? Was wird automatisch gemacht
### Erläuterung mit Mosquitto-Systemd und Docker-Mosquitto

## 100. Projekt starten
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