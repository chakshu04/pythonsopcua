import OpenOPC
import time
import paho.mqtt.client as paho

opc = OpenOPC.client()

IP ='localhost'
opc = OpenOPC.open_client(IP)
OPC_Name='Kepware.KEPServerEX.V6'
opc.connect( OPC_Name, IP)
Channel='Channel1.'
Device='Device1.'
Tag='Temp'
Data=opc.read('Channel1.Device1.Humidity')

print(Data)

broker="192.168.3.124"
port=1883
while True:
	def on_publish(client,userdata,result):             #create function for callback
    		print("data published \n")
	client1= paho.Client("control1")                           #create client object
	client1.on_publish = on_publish                          #assign function to callback
	client1.connect(broker,port)                                 #establish connection

	ret= client1.publish("device1",str(Data))     


	pass[2]