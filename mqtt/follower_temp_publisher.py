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
topic = "follower/temp"
client_id = 'follower_temp_publisher'
# client_id = f'python-mqtt-{random.randint(0,1000)}' for random id
username = USERNAME
password = PASSWORD


# temp_dummy_dict = {"shoulder_pan.temp": 0, "shoulder_lift.temp": 0, "elbow_flex.temp": 0, 
# "wrist_flex.temp": 0, "wrist_roll.temp": 0, "gripper.temp": 0}

# payload = json.dumps(temp_dummy_dict)


def main():
    clientCfg = utils.ClientCfg(client_id=client_id, port=port, broker=broker, username=username, password=password)
    client = utils.connect(clientCfg=clientCfg)
    client.loop_start()
    utils.example_publish(client=client, topic=topic)
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()