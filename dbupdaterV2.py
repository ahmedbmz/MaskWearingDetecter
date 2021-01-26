# USAGE
# python detect_mask_video.py

# import the necessary packages

import paho.mqtt.client as mqttClient
import credentiels
import pymysql.cursors


##################################################################
# In this part we will deal with the MQTT and MySQL connection code
##################################################################
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[INFO] Connected to broker")
        else:
            print("[ERROR] Connection failed")

    client = mqttClient.Client(credentiels.client_id)  # create new instance
    client.on_connect = on_connect  # attach function to callback
    client.connect(credentiels.mqttBroker, port=credentiels.mqttBrokerPort, keepalive=60)
    return client


# Save Data into DB Table
##################################################################
def subscribe(client: mqttClient):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        # Prepare Data, separate columns and values
        val = str(msg.payload.decode('utf-8')).split(" : ")
        convertedAccuracy = float(val[3])
        sql = "INSERT INTO detection (curenttime, state, color, accuracy) VALUES (%s, %s, %s, %s)"
        splitedValues = (val[0], val[1], val[2], convertedAccuracy)
        cursor = con.cursor()
        cursor.execute(sql, splitedValues)
        con.commit()
        print(cursor.rowcount, 'Data saved!')

    client.subscribe(credentiels.mqttTopic)
    client.on_message = on_message


try:
    con = pymysql.connect(host=credentiels.mysqlHost, user=credentiels.mysqlUser,
                          password=credentiels.mysqlPassword,
                          db=credentiels.dbName,
                          charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("MySQL Client Connected")
except:
    sys.exit("Connection to MySQL failed")
client = connect_mqtt()
subscribe(client)
client.loop_forever()  # start the loop
