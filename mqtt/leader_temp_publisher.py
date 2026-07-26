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
topic = "leader/temp"
client_id = 'leader_temp_publisher'
# client_id = f'python-mqtt-{random.randint(0,1000)}' for random id
# broker = BROKER
# port = PORT
# username = USERNAME
# password = PASSWORD


temp_dummy_dict = {"shoulder_pan.temp": 30, "shoulder_lift.temp": 30, "elbow_flex.temp": 30, 
                  "wrist_flex.temp": 30, "wrist_roll.temp": 30, "gripper.temp": 30}

payload = json.dumps(temp_dummy_dict)


def main():
    clientCfg = utils.ClientCfg(client_id=client_id)
    client = utils.connect(clientCfg=clientCfg)
    client.loop_start()
    utils.example_publish(client=client, topic=topic)
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()