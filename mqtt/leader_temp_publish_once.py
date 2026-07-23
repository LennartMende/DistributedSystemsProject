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
topic = "leader/temp"
client_id = 'leader_temp_publisher'
# client_id = f'python-mqtt-{random.randint(0,1000)}' for random id
username = USERNAME
password = PASSWORD

payload = {"shoulder_pan.temp": 5, "shoulder_lift.temp": 5, "elbow_flex.temp": 5, 
                  "wrist_flex.temp": 5, "wrist_roll.temp": 5, "gripper.temp": 5}
payload = {"shoulder_pan.temp": 15, "shoulder_lift.temp": 30, "elbow_flex.temp": 30, 
                  "wrist_flex.temp": 30, "wrist_roll.temp": 30, "gripper.temp": 30}
# temp_dummy_dict = {"shoulder_pan.temp": 5, "shoulder_lift.temp": 5, "elbow_flex.temp": 5, 
#                   "wrist_flex.temp": 5, "wrist_roll.temp": 5, "gripper.temp": 5}

# payload = json.dumps(temp_dummy_dict)


def main():
    clientCfg = utils.ClientCfg(client_id=client_id, port=port, broker=broker, username=username, password=password)
    client = utils.connect(clientCfg=clientCfg)
    utils.publish(client=client, topic=topic, data=payload, start_time=0)
    client.disconnect()

if __name__ == '__main__':
    main()