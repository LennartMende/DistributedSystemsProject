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

print(utils.__file__)

# setup
broker = BROKER
port = PORT
topic = "leader/vels"
client_id = 'leader_vel_subscriber'
# client_id = f'python-mqtt-{random.randint(0,1000)}' for random id
username = USERNAME
password = PASSWORD


def main():
    clientCfg = utils.ClientCfg(client_id=client_id, port=port, broker=broker, username=username, password=password)
    client = utils.connect(clientCfg=clientCfg)
    utils.subscribe(client=client, topic=topic)
    client.loop_forever()

if __name__ == '__main__':
    main()