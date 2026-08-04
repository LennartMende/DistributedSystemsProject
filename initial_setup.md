## Initiales Setup, um Projekt auf STM laufen zu lassen

# 1. Konfigurationsdatei ändern

Im (Linux) Host muss eine Konfigurationsdatei erstellt und der Listener hinzugefügt werden. Datei erstellen mit:

```bash
sudo vi /etc/mosquitto/conf.d/listener.conf
```

Und dann folgenden Inhalt einfügen:

```bash
listener 8883 0.0.0.0
allow_anonymous true
```

Im springbboot Ordner in src/main/ressources die Apllication.properties Datei Zeile 5 ändern:
```bash
robot.mqtt.broker = tcp://<Networkk_IP_Host>:8883
```



# 2. Userrechte setzen

In dem cert Ordner

```bash
chmod 644 *.key && chmod 644 *.p12
```




# 3. Mosquitto Broker auf dem Host starten

Mit:

```bash
systemctl start mosquitto
```


# 4. Publisher auf STM starten

In der mqtt/constants.py die Broker IP setzen auf 192.168.7.X. Also diese Zeile hier ändern:
```bash
BROKER = "<Network_IP_Host>"
```



Erstmal schauen, ob das hier passt:

```bash
ss -tulnp | grep 8883
```

Da muss bei USB z. B. `0.0.0.0:8883` stehen. Wenn nicht, dann den Mosquitto Server neu starten.

Und dann einfach den Publisher im mqtt Ordner starten mit:

```bash
python3 <name_of_publisher>.py
```
