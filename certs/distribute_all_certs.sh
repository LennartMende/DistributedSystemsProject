#!/bin/bash

set -e

# STM32
cp ca.crt ../stm32/certs/

cp client_control* ../stm32/certs/
cp client_dashboard* ../stm32/certs/
cp client_follower* ../stm32/certs/
cp client_leader* ../stm32/certs/


cp ca.crt ../stm32/lerobot/certs/

cp client_control* ../stm32/lerobot/certs/
cp client_dashboard* ../stm32/lerobot/certs/
cp client_follower* ../stm32/lerobot/certs/
cp client_leader* ../stm32/lerobot/certs/



# Mosquitto
cp ca.crt ../mosquitto/certs/

cp server.crt ../mosquitto/certs/
cp server.key ../mosquitto/certs/
cp server_7_27.crt ../mosquitto/certs/
cp server_7_27.key ../mosquitto/certs/

cp client_java* ../mosquitto/certs/

cp truststore.p12 ../mosquitto/certs/