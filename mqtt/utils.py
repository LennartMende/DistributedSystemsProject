from dataclasses import dataclass
import time
from paho.mqtt import client as mqtt_client
import json


@dataclass
class ClientCfg:
    client_id: str
    port: int
    broker: str
    username: str
    password: str


# connect a clientwith the broker
def connect(clientCfg: ClientCfg):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id=clientCfg.client_id)
    client.username_pw_set(clientCfg.username, clientCfg.password)
    client.on_connect = on_connect
    client.connect(clientCfg.broker, clientCfg.port)
    return client

# publishes data on the topic
def publish(client: mqtt_client.Client, topic):
    msg_count = 1
    while True:
        time.sleep(0.0167)
        msg = f"messages: {msg_count}"

        pos_dummy_dict = {
            "shoulder_pan": msg_count,
            "shoulder_lift": msg_count,
            "elbow_flex": msg_count,
            "wrist_flex": msg_count,
            "wrist_roll": msg_count,
            "gripper": msg_count
        }

        payload = json.dumps(pos_dummy_dict)
        
        result = client.publish(topic, payload)
        status = result.rc
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 3000:
            break

# subscribe data on the topic
def subscribe(client: mqtt_client.Client, topic):
    def on_message(client, user_data, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # print(f"Message = {msg}")
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
            print("JSON:", data)
        except json.JSONDecodeError:
            print("Received non‑JSON payload:", msg.payload)

    client.subscribe(topic)
    client.on_message = on_message