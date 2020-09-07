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

