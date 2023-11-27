import socket
import threading
import os

# Fonction pour recevoir des messages du serveur
def receive_messages(client_socket):
    try:
        while True:
            # Reçoit un message du serveur
            message = client_socket.recv(128).decode('utf-8')
            
            # Vérifie si le message est vide (connexion fermée par le serveur)
            if not message:
                break
            
            # Affiche le message
            print(message)
    except Exception as e:
        print(f"Erreur de réception : {e}")
    finally:
        # Ferme la connexion du client
        client_socket.close()
        print("La connexion au serveur a été fermée.")
        # Termine le processus du client
        os._exit(0)

# Crée un objet socket pour le client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définit l'hôte (adresse IP) et le port sur lequel le client se connectera
host, port = "127.0.0.1", 9999

# Se connecte au serveur
client.connect((host, port))

# Demande au client son nom
nom = input('Quel est votre nom ? ')
client.send(nom.encode('utf-8'))

# Envoie un message indiquant que le client a rejoint le chatroom
client.send(f"{nom} a rejoint le chatroom.".encode('utf-8'))

# Crée un thread pour recevoir les messages du serveur
thread_receive = threading.Thread(target=receive_messages, args=(client,))
thread_receive.start()

# Boucle principale du client pour envoyer des messages au serveur
while True:
    # Attend que l'utilisateur entre un message
    message = input(f"{nom} > ")

    # Envoie le message au serveur
    client.send(f"{nom} > {message}".encode('utf-8'))