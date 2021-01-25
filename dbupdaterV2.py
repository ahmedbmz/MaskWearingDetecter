# USAGE
# python detect_mask_video.py

# import the necessary packages

import paho.mqtt.client as mqttClient
import random


mqttBroker = "broker.emqx.io"
mqttBrokerPort = 1883
mqttUser = None
mqttPassword = None
mqtttopic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


##################################################################
#In this part we will deal with the MQTT and MySQL connection code
##################################################################
def connect_mqtt():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("[INFO] Connected to broker")
		else:
			print("[ERROR] Connection failed")

	client = mqttClient.Client(client_id)    #create new instance
	client.on_connect = on_connect           #attach function to callback
	client.connect(mqttBroker, port=mqttBrokerPort, keepalive=60)
	return client 

#Save Data into DB Table
##################################################################
def subscribe(client: mqttClient):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(mqtttopic)
    client.on_message = on_message

client = connect_mqtt()
subscribe(client)	
client.loop_forever()        #start the loop
