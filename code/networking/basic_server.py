#working 3/23
from socket import *
import os
import time

HOST = "192.168.1.101"
os.system('sudo ifconfig wlan0 down')
os.system('sudo ifconfig wlan0 ' + HOST)
os.system('sudo ifconfig wlan0 up')
os.system('ifconfig')
#print (HOST)

port = 12345
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
print ("Socket Made")
s.bind((HOST, port))
print ("Socket Bound")
s.listen(5)
print ("Listening for connections...")
q,addr = s.accept()
while True:
	data = time.time()
	q.send(bytes(data, "utf-8"))
        time.sleep(0.25)