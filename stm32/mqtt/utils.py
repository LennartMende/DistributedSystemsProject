from dataclasses import dataclass
from pathlib import Path
import time
from paho.mqtt import client as mqtt_client
import json

from constants import PORT, BROKER, USERNAME, PASSWORD

CERTS_DIR = Path(__file__).resolve().parent.parent / "certs"


@dataclass
class ClientCfg:
    client_id: str
    port: int = PORT
    broker: str = BROKER
    
    # Username + password:
    # username: str = USERNAME
    # password: str = PASSWORD

    # TLS:
    ca: str = str(CERTS_DIR / "ca.crt")
    @property
    def cert(self) -> str:
        return str(CERTS_DIR / f"client_{self.client_id}.crt")
    @property
    def key(self) -> str:
        return str(CERTS_DIR / f"client_{self.client_id}.key")


# connect a clientwith the broker
def connect(clientCfg: ClientCfg):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id=clientCfg.client_id)
    # client.username_pw_set(clientCfg.username, clientCfg.password) # for username + password
    # secure MQTT:
    ca_path = Path(clientCfg.ca)
    cert_path = Path(clientCfg.cert)
    key_path = Path(clientCfg.key)
    missing_files = [str(path) for path in (ca_path, cert_path, key_path) if not path.exists()]
    if missing_files:
        raise FileNotFoundError(f"Missing MQTT TLS files: {missing_files}")

    client.tls_set(
        ca_certs=str(ca_path),
        certfile=str(cert_path),
        keyfile=str(key_path)
    )
    client.tls_insecure_set(False)
    client.on_connect = on_connect
    client.connect(clientCfg.broker, clientCfg.port)
    return client

# publishes data on the topic
def example_publish(client: mqtt_client.Client, topic):
    phys_quantitiy = topic.split('/', 1)[1]
    msg_count = 1
    start_time = time.perf_counter()
    while True:
        time.sleep(0.0167)

        dummy_dict = {
            "shoulder_pan." + phys_quantitiy : msg_count,
            "shoulder_lift." + phys_quantitiy : msg_count,
            "elbow_flex." + phys_quantitiy : msg_count,
            "wrist_flex." + phys_quantitiy : msg_count,
            "wrist_roll." + phys_quantitiy : msg_count,
            "gripper." + phys_quantitiy : msg_count
        }

        payload_dict = {
            "processTimeStamp" : time.perf_counter() - start_time,
            "deviceId" : topic.split('/', 1)[0],
            "data" : dummy_dict
        }

        payload = json.dumps(payload_dict)
        
        result = client.publish(topic, payload)
        status = result.rc
        if status == 0:
            print(f"Sent `{payload}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 3000:
            break

# publishing a custom msg
def publish(client: mqtt_client.Client, topic: str, data: dict, start_time: float):
    payload_dict = {
        "processTimeStamp" : time.perf_counter() - start_time,
        "deviceId" : topic.split('/', 1)[0],
        "data" : data
    }
    msg: str = json.dumps(payload_dict)
    result = client.publish(topic, msg)
    status = result.rc
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    # msg_count += 1 if extern msg_count is passed as an argument

# subscribe data on the topic
def subscribe(client: mqtt_client.Client, topic):
    def on_message(client, user_data, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
            print(topic, ": ", data)
        except json.JSONDecodeError:
            print("Received non-JSON payload:", msg.payload)

    client.subscribe(topic)
    client.on_message = on_message
