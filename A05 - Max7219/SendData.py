#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "rcr/matrix"

def mqtt_on_connect( client, userdata, flags, rc ):
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC

    print( "Conectado con mqtt://{0}:{1}".format( MQTT_SERVER, MQTT_PORT ) )

def mqtt_on_message( client, userdata, msg ):
    print( msg.topic + " " +str( msg.payload ) )

def main():
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC

    mqttc = mqtt.Client()
    mqttc.on_connect = mqtt_on_connect
    mqttc.on_message = mqtt_on_message
    mqttc.loop_start()
    mqttc.connect( MQTT_SERVER, MQTT_PORT )
    time.sleep( 4 )

    for i in range( 0, 10 ):
        mqttc.publish( MQTT_TOPIC, str(i) )
        time.sleep( 1 )

    mqttc.loop_stop()
    mqttc.disconnect()

#####
main()
