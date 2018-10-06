#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import paho.mqtt.client as paho
import json
import time
import queue as Queue

MQTT_SERVER = "tron-ipst.freeddns.org"
MQTT_PORT = 1883
MQTT_TOPIC_IRCONTROL = "rcr/ircontrol"
MQTT_TOPIC_IRCONTROLS = {}
MQTT_TOPIC_IRCONTROLS['WINI'] = "rcr/ircontrol/01"

mqtt_client = None
messages = Queue.Queue()


def initIRCodes():
    global irCodes

    irCodes = {}
    irCodes['WINI'] = {}
    irCodes['WINI']['SLIDE FORWARD']  =  (6200,550, 1600,650, 600,1650, 1600,650, 600,1650, 1600,650, 1600,650, 600,1650, 600) #69D595CD
    irCodes['WINI']['SLIDE BACKWARD'] = (6150,550, 1600,650, 650,1600, 1600,650, 650,1600, 1600,650, 650,1600, 650,1600, 650)  #FD5FEC99
    irCodes['WINI']['WALK FORWARD']   = (6150,550, 1600,650, 600,1650, 1600,650, 650,1600, 600,1650, 600,1650, 600,1650, 1600) #3F32B1F2
    irCodes['WINI']['WALK BACKWARD']  = (6150,550, 1650,600, 650,1600, 1650,600, 650,1600, 650,1600, 1650,600, 650,1600, 1650) #A7432852
    #irCodes['WINI']['TURN LEFT'] = ()
    #irCodes['WINI']['TURN RIGHT'] = ()
    #irCodes['WINI']['VOLUME +'] = ()
    #irCodes['WINI']['VOLUME -'] = ()
    #irCodes['WINI']['STOP'] = ()
    #irCodes['WINI']['DEMO'] = ()
    #irCodes['WINI']['PATROL'] = ()
    #irCodes['WINI']['DANCE'] = ()
    #irCodes['WINI']['MUSIC'] = ()
    #irCodes['WINI']['PROGRAM'] = ()
    #irCodes['WINI']['MECHANICAL LANG'] = ()

def mqtt_on_message( client, userdata, message ):
    global messages

    try:
        messages.put_nowait( message )
    except:
        raise

def mqtt_on_connect( client, userdata, flags, rc ):
    global MQTT_SERVER, MQTT_PORT, MQTT_TOPIC_IRCONTROL

    client.subscribe( MQTT_TOPIC_IRCONTROL )
    print( '[IRemote] Conectado a mqtt://%s:%d/%s' % ( MQTT_SERVER, MQTT_PORT, MQTT_TOPIC_IRCONTROL ) )

def sendIRCodes( ircontrol, button ):
    global mqtt_client, irCodes, MQTT_TOPIC_IRCONTROLS

    try:
        data = irCodes[ircontrol][ button ]
        data = ''.join( [ '%04X' % x for x in data ] )
        mqtt_client.publish( MQTT_TOPIC_IRCONTROLS[ircontrol], data )
        time.sleep( 0.100 )
    except KeyError:
        pass
    except:
        raise

def main():
    global mqtt_client, MQTT_SERVER, MQTT_PORT

    print( '[IRemote] Iniciando...' )
    initIRCodes()
    mqtt_client = paho.Client()
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    while( True ):
        try:
            mqtt_client.connect( MQTT_SERVER, MQTT_PORT )
            break
        except Exception as e:
            print( '[IRemote] Servidor MQTT %s: %s' % ( MQTT_SERVER, e ) )
            time.sleep( 1 )
    mqtt_client.loop_start()
    abort = False
    while( not abort ):
        message = messages.get()
        message.payload = message.payload.decode( 'utf-8' )
        cmdLine = message.payload.strip().upper().split()
        print( '[IRemote] Mensaje recibido:', cmdLine )

        if( len(cmdLine) < 2 ):
            continue

        ircontrol = cmdLine.pop(0)
        cmdText = ' '.join( cmdLine )

        if( ircontrol == 'IRCONTROL' ):
            if( cmdLine[0] == 'EXIT' ):
                break
        else:
            sendIRCodes( ircontrol, cmdText );
    mqtt_client.loop_stop()
    print( '[IRemote] Finalizando...' )


#--
main()




