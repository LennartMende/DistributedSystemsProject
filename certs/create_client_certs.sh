#!/bin/bash

set -e

chmod +x create_java_certs.sh
chmod +x java_certs_conversion.sh

chmod +x create_python_arm_certs.sh
chmod +x create_python_control_dash_status_certs.sh


./create_java_certs.sh
./java_certs_conversion.sh

./create_python_arm_certs.sh
./create_python_control_dash_status_certs.sh
