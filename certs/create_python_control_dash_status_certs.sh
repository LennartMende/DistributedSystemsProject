#!/bin/bash

set -e

names=("client_control_subscriber" "client_dashboard_mode_subscriber" "client_system_state_publisher")

# names=("client_system_state_publisher")

for name in "${names[@]}"; do

    echo "Generating certificate for ${name}..."

    openssl genrsa -out "${name}.key" 4096

    openssl req \
        -new \
        -key "${name}.key" \
        -out "${name}.csr" \
        -config client.conf \
        -subj "/CN=${name}"

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
