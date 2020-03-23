#working 3/23
from socket import *
host = "192.168.1.101"
print (host)
port=12345
s=socket(AF_INET, SOCK_STREAM)
print ("socket made")
s.connect((host,port))
print ("socket connected!!!")
msg=s.recv(1024)
print ("Message from server : " + msg.decode("utf-8"))
