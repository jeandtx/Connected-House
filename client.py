import paho.mqtt.client as mqtt
import json
from jsonpath_ng import jsonpath, parse
from ac import clim


global temp, mode, fan
temp = 24
mode = 1
fan = 1
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("#")
    client.subscribe("zigbee2mqtt/+")
    client.subscribe("ac/+")

def on_message(client, userdata, msg):
    global temp, mode, fan

    if msg.topic == "ac/status":
        if msg.payload.decode("utf-8") == "0":
            clim(False, temp, mode, fan)
        else:
            clim(True, temp, mode, fan)

    elif msg.topic == "ac/temperature":
        temp = int(msg.payload.decode("utf-8"))
        clim(True, temp, mode, fan)
    elif msg.topic == "ac/mode":
        mode = int(msg.payload.decode("utf-8"))
        clim(True, temp, mode, fan)
    elif msg.topic == "ac/fan":
        fan = int(msg.payload.decode("utf-8"))
        clim(True, temp, mode, fan)




if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message


    client.connect("127.0.0.1", 1883, 60)
    client.publish("zigbee2mqtt/0x00158d000208e115", "Waiting .. ") # Door 
    client.publish("zigbee2mqtt/0x00158d000204c84f", "Waiting .. ") # Movement detector
    client.publish("zigbee2mqtt/0x00158d0002b5ac85", "Waiting .. ") # Temperature 
    client.publish("ac/temperature", "25")
    client.loop_forever()

