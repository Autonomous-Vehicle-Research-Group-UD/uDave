import socket
from datetime import datetime
import time 
import json

ServerAddress   = "127.0.0.1"
Port=20001

bufferSize          = 1024

# Create a UDP socket at client side
def open_socket(serverAddress, port):
	global ServerAddress,Port
	ServerAddress=serverAddress
	Port=port
	global UDPClientSocket 
	UDPClientSocket= socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	if UDPClientSocket:
		print('socket open: '+str(UDPClientSocket))
	else:
		print('sock open error')

# Send to server using created UDP socket

def senddata(address,x,y, speed, direction):
	data = str(address)+"|"+str(round(time.time() * 1000))+"|"+str(x)+"|"+str(y)+"|"+str(speed)+"|"+str(direction)
	
	UDPClientSocket.sendto(str.encode(data), (ServerAddress,Port))
	print("Msg sent: "+str(data))

def close_socket():	
	UDPClientSocket.close()
