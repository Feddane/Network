import socket
import threading
import os

# Fonction pour recevoir les messages du serveur
def receive_messages(client_socket):
    try:
        while True:
            # Recevoir le message du serveur
            message = client_socket.recv(128).decode('utf-8')
            # Vérifier si le message est vide (connexion fermée par le serveur)
            if not message:
                break
            # Afficher le message reçu
            print(message)
    except Exception as e:
        # Gérer les erreurs de réception
        print(f"Erreur de réception : {e}")
    finally:
        # Fermer le socket client
        client_socket.close()
        print("La connexion au serveur a été fermée.")
        # Terminer le programme
        os._exit(0)

# Créer un socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définir l'hôte et le port du serveur auquel le client se connectera
host, port = "127.0.0.1", 9999

# Se connecter au serveur
client.connect((host, port))

# Demander le nom de l'utilisateur
nom = input('Quel est votre nom ? ')
# Envoyer le nom au serveur
client.send(nom.encode('utf-8'))

# Envoyer un message indiquant que l'utilisateur a rejoint le chatroom
client.send(f"{nom} a rejoint le chatroom.".encode('utf-8'))

# Créer un thread pour recevoir les messages du serveur 
thread_receive = threading.Thread(target=receive_messages, args=(client,))
thread_receive.start()

# Boucle principale pour envoyer des messages au serveur
while True:
    # Demander à l'utilisateur d'entrer un message
    message = input(f"{nom} > ")
    # Envoyer le message au serveur
    client.send(f"{nom} > {message}".encode('utf-8'))
