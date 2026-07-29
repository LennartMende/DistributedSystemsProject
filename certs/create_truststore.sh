#!/bin/bash

set -e

keytool \
    -importcert \
    -alias mqtt-ca \
    -file ca.crt \
    -keystore truststore.p12 \
    -storetype PKCS12 \
    -storepass 123456 \
    -noprompt