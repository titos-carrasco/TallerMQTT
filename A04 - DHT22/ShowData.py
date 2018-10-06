#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "tron-ipst.freeddns.org"
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/dht22"

def mqtt_on_connect( client, userdata, flags, rc ):
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC

    print( "Conectado con mqtt://{0}:{1}".format( MQTT_SERVER, MQTT_PORT ) )

    client.subscribe( MQTT_TOPIC )
    print( 'Esperando en %s - %s' % ( MQTT_SERVER, MQTT_TOPIC ) )


def mqtt_on_message( client, userdata, msg ):
    print( msg.topic + " " +str( msg.payload ) )
    data = json.loads( msg.payload )

    nodo_id = data['id']
    temperatura = data['temperatura']
    humedad = data['humedad']
    print( "Temperatura: {0}° - Humedad: {1}%".format( temperatura, humedad ) )


def main():
    global MQTT_SERVER, MQTT_PORT

    mqttc = mqtt.Client()
    mqttc.on_connect = mqtt_on_connect
    mqttc.on_message = mqtt_on_message
    mqttc.loop_start()
    mqttc.connect( MQTT_SERVER, MQTT_PORT )
    time.sleep( 4 )

    for i in range( 60 ):
        time.sleep( 1 )

    mqttc.loop_stop()
    mqttc.disconnect()

#####
main()
