#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

# MQTT
import paho.mqtt.client as mqtt
import config
from time import sleep

import json
import datetime
import socket
 
# Sensors
from bme280i2c import BME280I2C

# LEDs
import RPi.GPIO as GPIO

verbose = 1

def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc), flush=True)
 
def on_disconnect(client, userdata, flag, rc):
    print("Disconnected with result code " + str(rc), flush=True)
    if rc != 0:
         print("Unexpected disconnection.", flush=True)
 
def on_publish(client, userdata, mid):
    if verbose > 1:
        print("publish: {0}".format(mid), flush=True)
 
def on_log(client, userdata, level, buff):
    if verbose > 1:
        print(buff, flush=True);

def main():
    use_led = False

    # LEDs
    if use_led:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)

    # Sensors
    bme280ch1 = BME280I2C(0x76)
    bme280ch2 = BME280I2C(0x77)
    r1 = bme280ch1.meas()
    r2 = bme280ch2.meas()
    if not (r1 or r2):
        print('No Sensor Available', flush=True)
    if r1:
        print('BME280 0x76', flush=True)

    # MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_log = on_log
    client.username_pw_set(config.username, config.password)
    client.connect(config.broker, 1883, 60) 

    data = {}
    data["device"] = str(socket.gethostname())
    data["payload"] = {}

    client.loop_start()
    try:
        if use_led:
            GPIO.output(17, 1)
        while True:
            #client.publish("hello/world","Hello, World!")
            r1 = bme280ch1.meas()
            if not r1:
                print('BME280 0x76 error', flush=True)
            data["payload"]["time"] = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            data["payload"]["temparature"] = str("{:.1f}".format(bme280ch1.T))
            data["payload"]["pressure"] = str("{:.1f}".format(bme280ch1.P))
            data["payload"]["humidity"] = str("{:.1f}".format(bme280ch1.H))
            if verbose > 1:
                print(data, flush=True)
            #print(json.dumps(data))
            client.publish("room1/data", format(json.dumps(data)))
            #client.publish("room1/temparature1","{:.1f}".format(bme280ch1.T))
            #client.publish("room1/pressure1","{:.1f}".format(bme280ch1.P))
            #client.publish("room1/humidity1","{:.1f}".format(bme280ch1.H))
            if use_led:
                GPIO.output(18, 1)
            sleep(1)
            if use_led:
                GPIO.output(18, 0)
            sleep(4)
            sleep(5)
    except KeyboardInterrupt:
        if use_led:
            GPIO.cleanup(17)
            GPIO.cleanup(18)
            GPIO.cleanup(22)
            GPIO.cleanup(27)
 
if __name__ == '__main__':
    main()
