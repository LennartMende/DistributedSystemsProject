#!/bin/bash

set -e

openssl genrsa -out server_7_27.key 4096

openssl req \
    -new \
    -key server_7_27.key \
    -out server_7_27.csr \
    -config server_san_7_27.cnf

openssl x509 \
    -req \
    -in server_7_27.csr \
    -CA ca.crt \
    -CAkey ca.key \
    -CAcreateserial \
    -out server_7_27.crt \
    -days 7300 \
    -sha256 \
    -extensions req_ext \
    -extfile server_san_7_27.cnf

rm server_7_27.csr

chmod 644 server_7_27.crt
chmod 644 server_7_27.key
