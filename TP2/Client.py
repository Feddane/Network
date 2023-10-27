import socket

client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = "127.0.0.1", 9999

client.connect((host, port))

nom = print('Quel est votre nom ?')

if __name__ == '__main__':
    while True:

        message = input(f"{nom} >")
        client.send(f"{nom} > {message}".encode("utf-8"))

