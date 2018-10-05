#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pip install pywws
# pip install pyusb
#

from __future__ import absolute_import, print_function
import datetime
import sys
import time

import pywws.logger
import pywws.weatherstation
import paho.mqtt.publish as publish
import json

def raw_dump(pos, data):
    print("%04x" % pos, end=' ')
    for item in data:
        print("%02x" % item, end=' ')
    print('')


def main():
    pywws.logger.setup_handler(False)
    ws = pywws.weatherstation.WeatherStation()
    raw_fixed = ws.get_raw_fixed_block()
    if not raw_fixed:
        print("No valid data block found")
        return 3

    #for ptr in range(0x0000, 0x0100, 0x20):
    #    raw_dump(ptr, raw_fixed[ptr:ptr+0x20])
    for data, ptr, logged in ws.live_data():
        #print( "---" )
        #print( ptr )
        #print( logged )
        del data['idx']
        print( data )
        publish.single( "rcr/weather",
          payload=json.dumps(data),
          hostname="test.mosquitto.org",
          port=1883)
    del ws
    return 0

main()
