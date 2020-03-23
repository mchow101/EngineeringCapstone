#working 3/23
from socket import *
import os
HOST = "192.168.1.101"
os.system('sudo ifconfig wlan0 down')
os.system('sudo ifconfig wlan0 ' + HOST)
os.system('sudo ifconfig wlan0 up')
os.system('ifconfig')
#print (HOST)
port = 12345
s = socket(AF_INET, SOCK_STREAM)
print ("Socket Made")
s.bind((HOST, port))
print ("Socket Bound")
s.listen(5)
print ("Listening for connections...")
while True:
	q,addr = s.accept()
	data = "Call me maybe"
	q.send(bytes(data))
