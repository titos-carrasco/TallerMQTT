#!/bin/bash

SERVER="test.mosquitto.org"
TOPIC="rcr/Speak"

echo "[Speak] Esperando en $SERVER - $TOPIC"
mosquitto_sub -h "$SERVER" -t "$TOPIC" | tee >(espeak -v mb/mb-vz1 -a 150 -s 160 -p 30 -g 0 -b 1)

