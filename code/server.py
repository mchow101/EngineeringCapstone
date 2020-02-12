from socket import *
import os
host = "172.20.27.97"
os.system('sudo ifconfig wlan0 down')
os.system('sudo ifconfig wlan0 ' + host)
os.system('sudo ifconfig wlan0 up')
print (host)
port = 7777
s = socket(AF_INET, SOCK_STREAM)
print ("Socket Made")
s.bind(("0.0.0.0", port))
print ("Socket Bound")
s.listen(5)
print ("Listening for connections...")
q,addr = s.accept()
data = "Call me maybe"
q.send(bytes(data))
