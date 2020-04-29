#working 3/23
import time
from socket import *

host = "192.168.1.106"
print (host)
port=12345
s=socket(AF_INET, SOCK_STREAM)
print ("socket made")
s.connect((host,port))
print ("socket connected!!!")
while True:
	msg=s.recv(1024)
	print ("Message from server : " + msg.decode("utf-8"))
	time.sleep(0.5)
