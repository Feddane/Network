import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port =  "127.0.0.1", 9999

server.bind((host, port))
print("Server started")

while True:
    server.listen(4)
    conn, adress = server.accept()
    print("Connection listening  ")

conn.close()
server.close()