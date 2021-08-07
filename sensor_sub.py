#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import paho.mqtt.client as mqtt
import config

import sqlite3
import json
 
class SensorManager:
    def __init__(self):
        self.dbname = 'room1.db'
        self.dbtable = 'sensor1'
        self.conn = sqlite3.connect(self.dbname)
        self.c = self.conn.cursor()

        checkdb = self.conn.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % self.dbtable)
        if checkdb.fetchone() == None:
            create_table = "create table {} (id integer primary key autoincrement, timestamp varchar(20), temp real, humid real, press real)".format(self.dbtable)
            self.c.execute(create_table)
            self.conn.commit()

    def on_connect(self, client, userdata, flag, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("room1/#") # Topic to subscribe
        #client.subscribe("room1/temparature1") # Topic to subscribe
        #client.subscribe("room1/pressure1") # Topic to subscribe
        #client.subscribe("room1/humidity1") # Topic to subscribe
 
    def on_disconnect(self, client, userdata, flag, rc):
        if rc != 0:
             print("Unexpected disconnection.")
 
    def on_message(self, client, userdata, msg):
        print("message: '{}' on topic {}".format(msg.payload, msg.topic))
        sql = 'insert into sensor1 (timestamp, temp, humid, press) values (?,?,?,?)'
        print(str(msg.payload.decode("utf-8","ignore")))
        recv = json.loads(str(msg.payload.decode("utf-8","ignore")))
        dv = recv["device"]
        pl = recv["payload"]
        data = (pl["time"], pl["temparature"], pl["humidity"], pl["pressure"])
        print(data)
        #self.conn = sqlite3.connect(self.dbname)
        #self.c = self.conn.cursor()
        self.c.execute(sql, data)
        self.conn.commit()
 
def main():
    mngr = SensorManager()

    client = mqtt.Client()
    client.on_connect = mngr.on_connect
    client.on_disconnect = mngr.on_disconnect
    client.on_message = mngr.on_message
    client.username_pw_set(config.username, config.password)
    client.connect(config.broker, 1883, 60) 
 
    client.loop_forever()
 
if __name__ == '__main__':
    main()
