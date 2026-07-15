Abhängigkeiten:
Python (z. B. in conda-env oder venv): paho-mqtt 2.1.0
apt: Maven 3.8.7, mosquitto 2.0.18
VSC: Spring Boot Dashboard, Spring Boot Extension Package, Spring Boot Tools, Spring Initializr Java Setup

Kurzanleitung:
- ein Terminal: in springboot-Verzeichnis wechseln und mvn spring-boot:run eingeben
- Browser: localhost:8080/api/robot/state oder localhost:8080/api/robot/posList
- zweites Termial: in mqtt-Verzeichnis wechseln und bei aktivierter env: python pos_publisher.py: anach sollte neue Werte in posList vorliegen


Quelle für Roboterarm-Favicon:
<a href="https://www.flaticon.com/de/kostenlose-icons/roboter" title="roboter Icons">Roboter Icons erstellt von smalllikeart - Flaticon</a>
https://icon-icons.com/de/symbol/roboter/4899?ii_item_modal=1&ii_modal_origin=%2Fde%2Fsuche%2Fsymbole%2Froboter