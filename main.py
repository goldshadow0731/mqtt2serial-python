# -*- coding: UTF-8 -*-
import os

from paho.mqtt.client import Client
import serial


client = Client()


@client.connect_callback()
def on_connect(client: Client, userdata, flags, result):
    print(f"=============== {'Connected':^15s} ===============")


@client.disconnect_callback()
def on_disconnect(client: Client, userdata, result):
    print(f"=============== {'Disconnected':^15s} ===============")


if __name__ == "__main__":
    try:
        client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")))
        while True:
            with serial.Serial(os.getenv("SERIAL_PORT"), int(os.getenv("SERIAL_BAUDRATE"))) as port:
                client.publish(os.getenv("MQTT_TOPIC"),
                               port.readline().decode().rstrip("\r\n"))
    except:
        pass
