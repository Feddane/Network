import socket
import threading
import  os

# Fonction pour gérer la réception des messages du serveur
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(128).decode('utf-8') #decode le message et le mettre dans message
            if not message:  #message vide
                break
            print(message)
    except Exception as e:  #si une connexion a ete interompue ou si on execute en premier le fichier client
        print(f"Erreur de réception : {e}")
    finally:
        client_socket.close()
        print("La connexion au serveur a été fermée.")
        os._exit(0) #terminer le programme de manière brutale


# Création du socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définition de l'adresse et du port du serveur
host, port = "127.0.0.1", 9999

# Tentative de connexion au serveur
client.connect((host, port))

# Demande du nom de l'utilisateur
nom = input('Quel est votre nom ? ')

# Envoi du nom au serveur
client.send(f"{nom} a rejoint le chatroom.".encode('utf-8'))

# Création d'un thread pour recevoir les messages en parallèle
thread_receive = threading.Thread(target=receive_messages, args=(client,)) #Cela crée un nouvel objet de thread appelé thread_receive. L'argument target spécifie la fonction que le thread exécutera, et args spécifie les arguments à passer à cette fonction. Dans ce cas, le thread exécutera la fonction receive_messages et passera le socket du client client comme argument.
thread_receive.start()
    #En résumé, ces trois lignes de code créent un thread (thread_receive) 
    # qui exécute la fonction receive_messages en arrière-plan. 
    # Cela permet au programme principal de continuer son exécution, 
    # notamment d'envoyer des messages depuis l'utilisateur, sans être bloqué par 
    # la fonction de réception des messages du serveur. 
    # Le thread créé s'occupe de manière asynchrone de la réception des messages du serveur 
    # tout en permettant à l'utilisateur d'interagir avec l'interface utilisateur principale de l'application.

# Boucle principale pour envoyer des messages
while True:
    message = input(f"{nom} > ")
    client.send(f"{nom} > {message}".encode('utf-8'))




#thread == L'utilisation de threads permet d'accomplir plusieurs tâches en parallèle, sans bloquer l'exécution du programme