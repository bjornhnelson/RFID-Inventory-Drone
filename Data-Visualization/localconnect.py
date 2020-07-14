# To run do the following:
#   Connect the master tag
#   Connect 4 anchors
#   Connect the regular tag that will be tracked
#   Open the Pozyx software
#   Connect and calibrate all tags and anchors
#   Run this script from the terminal with:
#      python localconnect.py > position.json
#   This will create a position.json file that will be updated live until a cntl+c

import paho.mqtt.client as mqtt
import ssl

host = "localhost"
port = 1883
topic = "tags" 

def on_connect(client, userdata, flags, rc):
    #print(mqtt.connack_string(rc))
    mqtt.connack_string(rc)

# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    print(msg.payload.decode())
    msg.payload.decode()

def on_subscribe(client, userdata, mid, granted_qos):
#    print("Subscribed to topic!")


client = mqtt.Client()

# set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)

# works blocking, other, non-blocking, clients are available too.
client.loop_forever()
