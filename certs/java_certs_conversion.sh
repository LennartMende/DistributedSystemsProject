#!/bin/bash

set -e

for name in \
  client_java_subscriber \
  client_java_control_publisher \
  client_java_dashboard_mode_publisher \
  client_java_system_state_subscriber
do
  openssl pkcs12 -export \
    -in ${name}.crt \
    -inkey ${name}.key \
    -out ${name}.p12 \
    -name ${name} \
    -CAfile ca.crt \
    -caname root \
    -passout pass:123456
done
