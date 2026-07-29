#!/bin/bash

set -e

openssl genrsa -out ca.key 4096

openssl req \
    -new \
    -x509 \
    -days 7300 \
    -key ca.key \
    -out ca.crt \
    -subj "/CN=SOARM-CA"