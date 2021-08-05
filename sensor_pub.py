#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# MQTT
import paho.mqtt.client as mqtt
import config
from time import sleep

# Sensors
from bme280i2c import BME280I2C
 
def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))
 
def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
         print("Unexpected disconnection.")
 
def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))
 
def main():
    # Sensors
    bme280ch1 = BME280I2C(0x76)
    bme280ch2 = BME280I2C(0x77)
    r1 = bme280ch1.meas()
    r2 = bme280ch2.meas()
    if not (r1 or r2):
        print('No Sensor Available')
    if r1:
        print('BME280 0x76')

    # MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.username_pw_set(config.username, config.password)
    client.connect(config.broker, 1883, 60) 
 
    client.loop_start()
    while True:
        #client.publish("hello/world","Hello, World!")
        client.publish("room1/temparature1","{:.1f}".format(bme280ch1.T))
        client.publish("room1/pressure1","{:.1f}".format(bme280ch1.P))
        client.publish("room1/humidity1","{:.1f}".format(bme280ch1.H))
        sleep(3)
 
if __name__ == '__main__':
    main()
