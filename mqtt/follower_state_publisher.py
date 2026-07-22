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
topic = "follower/state"
client_id = 'follower_state_publisher'
# client_id = f'python-mqtt-{random.randint(0,1000)}' for random id
username = USERNAME
password = PASSWORD


state_dummy_dict = {"state": "RUNNING"}

payload = json.dumps(state_dummy_dict)


def main():
    clientCfg = utils.ClientCfg(client_id=client_id, port=port, broker=broker, username=username, password=password)
    client = utils.connect(clientCfg=clientCfg)
    client.loop_start()
    utils.publish(client=client, topic=topic, payload=state_dummy_dict)
    client.disconnect()

if __name__ == '__main__':
    main()