import argparse
import time
import OpenOPC


parser = argparse.ArgumentParser()
parser.add_argument("-ip", action="store", required=True, dest="ipaddress", help="ip of the modbus slave")
parser.add_argument("-OPC", action="store", required=True, dest="OPC", help="name of the opc server")
parser.add_argument("-channel", action="store", required=True, dest="channel", help="channel address to be read")
parser.add_argument("-device", action="store", required=True, dest="device", help="device address to be read")
parser.add_argument("-tag", action="store", required=True, dest="tag", help="tag address to be read")
#parser.add_argument("-fun", action="store", required=True, dest="fun", help="function")
#parser.add_argument("-t", action="store", required=True, dest="time", help="time delay")
#parser.add_argument("-dt", action="store", required=True, dest="datatype", help="datatype")

args = parser.parse_args()

opc = OpenOPC.client()

IP =args.ipaddress
opc = OpenOPC.open_client(IP)
OPC_Name=args.OPC
opc.connect( OPC_Name, IP)
Channel=args.channel
Device=args.device
Tag=args.tag
Data=opc.read(Channel.Device.Tag)

print(Data)

