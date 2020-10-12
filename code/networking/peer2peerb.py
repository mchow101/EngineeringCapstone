import time
from socket import *
import threading

host = "IP"
print(host)
port_in = 5000
port_out = 5003

# make socket
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
print("Socket Made")

# receive messages
def get_msg():
    s.connect((host, port_in))
    print("socket connected!!!")
    if __name__ == '__main__':
        while True:
            try:
                msg = s.recv(1024)
                print("Message from server : " + msg.decode("utf-8"))
                time.sleep(0.5)
            except (KeyboardInterrupt):
                print("Stopped")

# send messages
def send_msg():
    if __name__ == '__main__':
        s.bind(('', port_out))
        print("Socket Bound")
        s.listen(5)
        print("Listening for connections...")
        try:
            q, addr = s.accept()
            while not s.shutdown:
                data = time.time()
                q.send(bytes(data, "utf-8"))
                time.sleep(0.25)
        except (KeyboardInterrupt):
            print("Stopped")

# start client
client = threading.Thread(target=get_msg)
# client.daemon = True
client.start()

# start server
server = threading.Thread(target=send_msg)
server.start()
