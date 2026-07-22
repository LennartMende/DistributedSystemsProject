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
    # secure MQTT:
    # client.tls_set(
    #     ca_certs="../certs/ca.crt",
    #     certfile=f"../certs/client_{clientCfg.client_id}.crt",
    #     keyfile=f"../certs/client_{clientCfg.client_id}.key"
    # )
    # client.tls_insecure_set(False)
    client.on_connect = on_connect
    client.connect(clientCfg.broker, clientCfg.port)
    return client

# publishes data on the topic
def example_publish(client: mqtt_client.Client, topic):
    phys_quantitiy = topic.split('/', 1)[1]
    msg_count = 1
    while True:
        time.sleep(0.0167)
        msg = f"messages: {msg_count}"

        pos_dummy_dict = {
            "shoulder_pan." + phys_quantitiy : msg_count,
            "shoulder_lift." + phys_quantitiy : msg_count,
            "elbow_flex." + phys_quantitiy : msg_count,
            "wrist_flex." + phys_quantitiy : msg_count,
            "wrist_roll." + phys_quantitiy : msg_count,
            "gripper." + phys_quantitiy : msg_count
        }

        payload = json.dumps(pos_dummy_dict)

        print("payload = ", payload)
        
        result = client.publish(topic, payload)
        status = result.rc
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 3000:
            break

# publishing a custom msg
def publish(client: mqtt_client.Client, topic, payload: dict):
    msg: str = json.dumps(payload)
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
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # print(f"Message = {msg}")
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
            print(topic, data)
        except json.JSONDecodeError:
            print("Received non‑JSON payload:", msg.payload)

    client.subscribe(topic)
    client.on_message = on_message