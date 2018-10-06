#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

import paho.mqtt.client as paho
from rcr.robots.fluke2.Fluke2 import Fluke2
from rcr.utils import Utils
import json
import time
import queue
import unicodedata

MQTT_SERVER = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_TOPIC  = 'rcr/S2'

messages = queue.Queue( 1 )

def mqtt_on_connect( client, userdata, flag, rc ):
    """Invocada al conectar a servidor MQTT."""
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC

    client.subscribe( MQTT_TOPIC )
    print( "[S2] Esperando en mqtt://%s:%d/%s" % ( MQTT_SERVER, MQTT_PORT, MQTT_TOPIC ) )

def mqtt_on_message( client, userdata, message ):
    """Invocada al recibir mensaje MQTT en algun topico suscrito."""
    global messages

    # si no se ha procesado el ultimo mensaje lo eliminamos
    try:
        messages.get_nowait()
    except queue.Empty:
        pass

    # agregamos el mensaje
    try:
        messages.put_nowait( message )
    except queue.Full:
            pass


def main():
    """Realiza pruebas del S2 recibiendo comandos via MQTT."""
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC, messages

    robot = Fluke2( port="/dev/rfcomm2", bauds=9600, timeout=500 )

    mqtt_client = paho.Client()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
    mqtt_client.loop_start()

    abort = False
    while( not abort ):
        message = messages.get()
        cmd = message.payload.decode( 'utf-8' ).lower().strip()
        print( "[S2] Mensaje recibido:", cmd )

        if( cmd == 'exit' ):
            abort = True
        elif( cmd == 'name' ):
            print( robot.s2Inner.getName() )
        elif( cmd == 'left' ):
            robot.getS2Motors().setMotors( -100, 100 )
        elif( cmd == 'right' ):
            robot.getS2Motors().setMotors( 100, -100 )
        elif( cmd == 'forward' ):
            robot.getS2Motors().setMotors( 50, 50 )
        elif( cmd == 'backward' ):
            robot.getS2Motors().setMotors( -50, -50 )
        elif( cmd == 'stop' ):
            robot.getS2Motors().setMotors( 0, 0 )

    mqtt_client.loop_stop()
    robot.close()

if( __name__ == "__main__" ):
    main()
