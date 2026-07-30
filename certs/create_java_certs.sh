#!/bin/bash

set -e

names=("client_java_control_publisher" "client_java_dashboard_mode_publisher" "client_java_subscriber" "client_java_system_state_subscriber")

# names=("client_java_system_state_subscriber")

for name in "${names[@]}"; do

    echo "Generating certificate for ${name}..."

    openssl genrsa -out "${name}.key" 4096

    openssl req \
        -new \
        -key "${name}.key" \
        -out "${name}.csr" \
        -config client.conf \
        -subj "/CN=${arm}_${quantity}_${client}"

    openssl x509 \
        -req \
        -in "${name}.csr" \
        -CA ca.crt \
        -CAkey ca.key \
        -CAcreateserial \
        -out "${name}.crt" \
        -days 7300 \
        -sha256

    rm "${name}.csr"

done

echo "Done!"
