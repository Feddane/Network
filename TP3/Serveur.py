import socket
import select

# Créer un objet socket pour le serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définir l'hôte et le port sur lequel le serveur écoutera
host, port = "127.0.0.1", 9999

# Lier le serveur à l'hôte et au port spécifiés
server.bind((host, port))
# Définir le nombre maximal de connexions en attente
server.listen(5)

# Créer une liste contenant le socket du serveur
socket_objs = [server]

# Afficher un message de bienvenue
print("Bienvenue dans le chatroom !!!")

# Ajouter un dictionnaire pour stocker les noms associés aux sockets clients
client_noms = {}

# Fonction pour diffuser un message à tous les clients sauf à l'émetteur
def broadcast(server_socket, sender_socket, message):
    for socket_obj in socket_objs:
        if socket_obj != server_socket and socket_obj != sender_socket:
            try:
                socket_obj.send(f"{message}".encode('utf-8'))
            except:
                # Gérer les erreurs de connexion et supprimer le socket défectueux
                socket_objs.remove(socket_obj)

# Boucle principale du serveur
while True:
    # Utiliser select pour surveiller les sockets en lecture
    list_lue, list_accee_Ecrit, exception = select.select(
        socket_objs, [], socket_objs)

    # Parcourir les sockets prêts à être lus
    for socket_obj in list_lue:
        # Vérifier si le socket en cours est le socket du serveur
        if socket_obj is server:
            # Accepter la connexion du client
            client, address = server.accept()
            # Ajouter le socket client à la liste des sockets
            socket_objs.append(client)
            # Demander le nom au client
            client_name = client.recv(128).decode('utf-8')
            # Associer le nom du client à son socket dans le dictionnaire
            client_noms[client] = client_name

            # Afficher un message indiquant qu'un nouveau participant a rejoint le chatroom
            print(f"Nouveau participant {client_name} connecté depuis {address}")
            # Diffuser le message à tous les clients
            broadcast(server, client, f"{client_name} a rejoint le chatroom.")
        else:
            try:
                # Recevoir des données du client
                donnees_recues = socket_obj.recv(128).decode('utf-8')

                if donnees_recues:
                    # Afficher les données reçues
                    print(donnees_recues)
                    # Diffuser le message à tous les clients
                    broadcast(server, socket_obj, donnees_recues)
            except ConnectionResetError:
                # Gérer les erreurs de connexion et supprimer le socket défectueux
                socket_objs.remove(socket_obj)
                # Afficher un message indiquant qu'un client s'est déconnecté
                print(client_noms[socket_obj] + " s'est déconnecté")
                # Diffuser le message à tous les clients
                broadcast(server, socket_obj, client_noms[socket_obj] + " s'est déconnecté.")
                # Afficher le nombre de participants restants
                print(f"{len(socket_objs) - 1} participants restants")
