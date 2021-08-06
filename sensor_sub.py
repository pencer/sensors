#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import paho.mqtt.client as mqtt
import config
 
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))
  client.subscribe("hello/world") # Topic to subscribe
 
def on_disconnect(client, userdata, flag, rc):
  if rc != 0:
     print("Unexpected disconnection.")
 
def on_message(client, userdata, msg):
  print("message: '{}' on topic {}".format(msg.payload, msg.topic))
 
def main():
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_disconnect = on_disconnect
  client.on_message = on_message
  client.username_pw_set(config.username, config.password)
  client.connect(config.broker, 1883, 60) 
 
  client.loop_forever()
 
if __name__ == '__main__':
  main()
