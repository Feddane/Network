import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port =  "127.0.0.1", 9999

try:
    client.connect((host, port))
    print("client connected")
except:
    print("connection to server failed")
finally:
    client.close()