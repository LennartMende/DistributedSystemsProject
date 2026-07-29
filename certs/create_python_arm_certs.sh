#!/bin/bash

set -e

arms=("leader" "follower")
quantities=("pos" "temp" "volt")
clients=("publisher" "subscriber")

for arm in "${arms[@]}"; do
    for quantity in "${quantities[@]}"; do
        for client in "${clients[@]}"; do

            NAME="client_${arm}_${quantity}_${client}"

            echo "Generating certificate for ${NAME}..."

            openssl genrsa -out "${NAME}.key" 4096

            openssl req \
                -new \
                -key "${NAME}.key" \
                -out "${NAME}.csr" \
                -config client.conf \
                -subj "/CN=${arm}_${quantity}_${client}"

            openssl x509 \
                -req \
                -in "${NAME}.csr" \
                -CA ca.crt \
                -CAkey ca.key \
                -CAcreateserial \
                -out "${NAME}.crt" \
                -days 7300 \
                -sha256

            rm "${NAME}.csr"

        done
    done
done

echo "Done!"