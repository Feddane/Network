import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#definition de l'adresse et du port du serveur auquel le client tente de se connecter
host, port =  "127.0.0.1", 9999

try:
    client.connect((host, port))
    print("client connecté")
except:
    print("connection au serveut echouée !!!")
finally:
    client.close()