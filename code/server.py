from socket import *
host = "192.168.43.64"
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
q.send(bytes(data, "utf-8"))