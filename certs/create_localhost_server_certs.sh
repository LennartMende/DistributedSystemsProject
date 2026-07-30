#!/bin/bash

set -e

openssl genrsa -out server.key 4096

openssl req \
    -new \
    -key server.key \
    -out server.csr \
    -config san.cnf

openssl x509 \
    -req \
    -in server.csr \
    -CA ca.crt \
    -CAkey ca.key \
    -CAcreateserial \
    -out server.crt \
    -days 7300 \
    -sha256 \
    -extensions req_ext \
    -extfile san.cnf

rm server.csr

chmod 644 server.crt
chmod 644 server.key