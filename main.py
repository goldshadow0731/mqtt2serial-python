# -*- coding: UTF-8 -*-
import os

from paho.mqtt.client import Client, MQTTMessage
import serial


client = Client()
port = serial.Serial(os.getenv("SERIAL_PORT"),
                     int(os.getenv("SERIAL_BAUDRATE")))


@client.connect_callback()
def on_connect(client: Client, userdata, flags, result):
    print(f"=============== {'Connected':^15s} ===============")
    if os.getenv("MQTT_RECEIVE_TOPIC", None):
        client.subscribe(os.getenv("MQTT_RECEIVE_TOPIC"))


@client.disconnect_callback()
def on_disconnect(client: Client, userdata, result):
    print(f"=============== {'Disconnected':^15s} ===============")


def on_message(client: Client, userdata, msg: MQTTMessage):
    if port.is_open:
        port.write(msg.payload)
        port.write(b"\r\n")


client.on_message = on_message if os.getenv("MQTT_RECEIVE_TOPIC") else None


if __name__ == "__main__":
    try:
        client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")))
        client.loop_start()
        if not port.is_open:
            port.open()
        if not port.is_open:
            raise serial.SerialException("Serial port open failed.")
        while True:
            client.publish(os.getenv("MQTT_SEND_TOPIC"),
                           port.readline().decode().rstrip("\r\n"))
    except:
        port.close()
        client.loop_stop()
