"""
CLI subscription:
in general: mosquitto_sub -h <broker> -u <username> -P <password> -t <topic>
e.g.: mosquitto_sub -h broker.emqx.io -u nansoren -P 88 -t python/mqtt
"""

from constants import BROKER, PORT, USERNAME, PASSWORD

import random
import logging
import time
from paho.mqtt import client as mqtt_client
import utils
import json

# setup
broker = BROKER
port = PORT
topic = "leader/volt"
client_id = 'leader_volt_publisher'
# client_id = f'python-mqtt-{random.randint(0,1000)}' for random id
username = USERNAME
password = PASSWORD

payload = {"shoulder_pan.volt": 6, "shoulder_lift.volt": 5, "elbow_flex.volt": 5, 
                  "wrist_flex.volt": 5, "wrist_roll.volt": 5, "gripper.volt": 5}

# volt_dummy_dict = {"shoulder_pan.volt": 5, "shoulder_lift.volt": 5, "elbow_flex.volt": 5, 
#                   "wrist_flex.volt": 5, "wrist_roll.volt": 5, "gripper.volt": 5}

# payload = json.dumps(volt_dummy_dict)


def main():
    clientCfg = utils.ClientCfg(client_id=client_id, port=port, broker=broker, username=username, password=password)
    client = utils.connect(clientCfg=clientCfg)
    utils.publish(client=client, topic=topic, payload=payload)
    client.disconnect()

if __name__ == '__main__':
    main()