import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import pymysql.cursors
import json
import credentiels
		 
#############################
#credentiels to connect to broker and MySQL
#############################
# User variables for MQTT Broker connection
mqttBroker = "broker.emqx.io"
mqttBrokerPort = 1883
mqttUser = None
mqttPassword = None
mqtttopic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# User variables for MQTT Broker connection
mysqlHost = "bbzj937svfngzjrooibe-mysql.services.clever-cloud.com"
mysqlUser = "uaxb8xwaqzqfhyg5"
mysqlPassword = "TzBw8FtF0rB9hSVsPXye"
dbName= "bbzj937svfngzjrooibe"

# Function used for MySQL database connection
# Returns a connection object
def sql_connect():
	conn = pymysql.connect( host = mysqlHost,
                            user = mysqlUser,
                            password = mysqlPassword,
                            db = 'dbName',
                            charset = 'utf8mb4',
                            cursorclass = pymysql.cursors.DictCursor)

	print( "Connected to DB" )
	return conn
	
	
# Function used to perform an insert query into the DB
def sql_insert( conn, args ):
	with conn.cursor() as cursor:
		sql = "INSERT INTO `detection` (`curenttime`, `state` ,`color`,`accuracy`) VALUES (%s, %s , %s , %.2f )"
		sor.execute( sql, ( args[0], args[1] ,args[2],args[3]) )
	conn.commit()
	

# Function used to receive message from the MQTT broker
# Takes as argument the hostname, the port and the topic
# Returns the message payload
def receive( host, port, topic ):
	msg = subscribe.simple( topic, hostname = host, port = port )
	return msg


def main():
	
	print( "DB process starting..." )
	
	# Connect to the database
	conn = sql_connect()
	
	saved = [False, False]
	
	while( True ):
		# Subscribe topic and receive messages
		msg = receive( mqttBroker, mqttBrokerPort, mqtttopic
		
		# Working on data to avoid error on mysql insert
		msg = json.loads( msg.payload )
		
		data = '{'
		
		for key in msg["data"]:
			data += '"' + key + '": "' + str( msg["data"][key] ) + '", '
		k = data.rfind(', ')
		data = data[:k] + data[k+1:]	
		
		data += '}'	

		# Insert into DB
		if( not saved[int(msg["id"])-1] ):
			sql_insert( conn, [msg["id"], data] )
			print( msg["id"] + " -> " + data )
			saved[int(msg["id"])-1] = True
		
		# Sleep
		if( saved[0] and saved[1] ):
			time.sleep( config.SLEEP_TIME )
			saved = [False, False]
			
if __name__== "__main__":
	main()