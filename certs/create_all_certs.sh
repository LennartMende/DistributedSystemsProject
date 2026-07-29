#!/bin/bash

set -e

chmod +x create_ca.sh
chmod +x create_client_certs.sh
chmod +x create_localhost_server_certs.sh
chmod +x create_server_7_27_certs.sh
chmod +x create_truststore.sh

./create_ca.sh
./create_client_certs.sh
./create_localhost_server_certs.sh
./create_server_7_27_certs.sh
./create_truststore.sh