import socket
import select

# Création du socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définition de l'adresse et du port
host, port = "127.0.0.1", 9999

# Liaison du serveur à l'adresse et au port spécifiés
server.bind((host, port))
server.listen(5)  # Permet jusqu'à 5 connexions en attente

# Liste des sockets (serveur inclus) pour la gestion avec select
socket_objs = [server]

print("Bienvenue dans le chatroom !!!")

# Fonction pour diffuser un message à tous les clients
def broadcast(server_socket, sender_socket, message):
    for socket_obj in socket_objs:
        # Envoyer le message à tous les clients, sauf à l'expéditeur et au serveur
        if socket_obj != server_socket and socket_obj != sender_socket:
            try:
                socket_obj.send(message.encode('utf-8'))
            except:
                # Gérer les erreurs d'envoi (peut se produire si le client est déconnecté) pour pas que le client envoi des msg a des clients deconnectes
                socket_objs.remove(socket_obj)

while True:
    list_lue, list_accee_Ecrit, exception = select.select(
        socket_objs, [], socket_objs)

    for socket_obj in list_lue:
        if socket_obj is server:
            # Nouvelle connexion entrante
            client, address = server.accept()
            socket_objs.append(client)
            print(f"Nouveau participant connecte depuis {address}")
            broadcast(server, client, f"{address} a rejoint le chatroom.")
        else:
            # Réception de données d'un client connecté
            try:
                donnees_recus = socket_obj.recv(128).decode('utf-8')

                if donnees_recus:
                    print(donnees_recus)
                    # Diffuser le message à tous les clients
                    broadcast(server, socket_obj, donnees_recus)
            except ConnectionResetError:
                # Le client s'est déconnecté
                socket_objs.remove(socket_obj)
                print(f"Un participant est deconnecte")
                broadcast(server, socket_obj, "Un participant s'est deconnecte.")
                print(f"{len(socket_objs) - 1} participants restants")

