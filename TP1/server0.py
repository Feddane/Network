import socket

# Création du socket du serveur, SOCK_STREAM = pour les connexions TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Définition de l'adresse et du port du serveur
host, port =  "127.0.0.1", 9999

#liaison du serveur à l'adresse et au port spécifiés
server.bind((host, port))
print("Le serveur est démarré")

while True:
    server.listen(4) # le serveur peut accepter jusqu'à 4 connexions en attente.
    conn, address = server.accept()
    print("Serveur en écoute  ")

    conn.close()
server.close()