import os
import random
import json
from paho.mqtt import client as mqtt_client

broker = '192.168.3.206'
port = 1883
topic = "sys/deploy"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        cmds = json.loads(msg.payload.decode())
        print("cmd = %s, name = %s, image = %s" % (cmds["cmd"], cmds["name"], cmds["image"]))
        if cmds["cmd"] == "install":
            print("begin to deploy")
            os.system("kubectl run %s --image=%s" % (cmds["name"], cmds["image"]))
            print("done")
        else:
            print("begin to remove")
            os.system("kubectl delete pod %s" % cmds["name"])
            print("done")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

