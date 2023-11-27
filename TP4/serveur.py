import socket
import threading
import select

# Crée un objet socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définit l'hôte (adresse IP) et le port sur lequel le serveur écoutera
host, port = "127.0.0.1", 9999

# Associe le serveur à l'adresse et au port spécifiés
server.bind((host, port))

# Configure le serveur pour écouter jusqu'à 5 connexions simultanées
server.listen(5)

# Liste des objets socket, y compris le serveur lui-même
socket_objs = [server]

# Affiche un message de bienvenue
print("Bienvenue dans le chatroom !!!")

# Dictionnaire pour stocker les noms des clients
client_noms = {}

# Fonction pour gérer la connexion d'un client
def handle_client_connection(client_socket):
    try:
        while True:
            # Reçoit des données du client
            data = client_socket.recv(128).decode('utf-8')

            # Si le client se déconnecte, le retire de la liste des sockets (s'il est encore présent)
            if not data:
                if client_socket in socket_objs:
                    socket_objs.remove(client_socket)
                    print(f"{client_noms[client_socket]} s'est déconnecté")
                    broadcast(server, client_socket, f"{client_noms[client_socket]} s'est déconnecté.")
                continue

            # Traite le message reçu
            message = f"{data}"
            print(message)
            broadcast(server, client_socket, message)

    except:
        if client_socket in socket_objs:
            socket_objs.remove(client_socket)
            print(f"{client_noms[client_socket]} s'est déconnecté")
            broadcast(server, client_socket, f"{client_noms[client_socket]} s'est déconnecté.")
            print(f"{len(socket_objs) - 1} participants restants")

# Fonction pour diffuser un message à tous les clients sauf l'émetteur
def broadcast(server_socket, sender_socket, message):
    for socket_obj in socket_objs:
        if socket_obj != server_socket and socket_obj != sender_socket:
            try:
                socket_obj.send(message.encode('utf-8'))
            except:
                socket_objs.remove(socket_obj)

# Boucle principale du serveur
while True:
    # Utilise select pour surveiller les sockets prêts à être lus, écrits, ou en erreur
    readable_sockets, _, _ = select.select(socket_objs, [], socket_objs)

    # Parcourt les sockets prêts à être lus
    for socket_obj in readable_sockets:
        if socket_obj is server:
            # Nouvelle connexion entrante
            client, address = server.accept()
            socket_objs.append(client)

            # Demande au client son nom
            client_name = client.recv(128).decode('utf-8')
            client_noms[client] = client_name

            print(f"Nouveau participant {client_name} connecté depuis {address}")
            broadcast(server, client, f"{client_name} a rejoint le chatroom.")

            # Crée un thread pour gérer la connexion du client
            thread = threading.Thread(target=handle_client_connection, args=(client,))
            thread.start()
        else:
            # Gère les messages entrants des clients existants
            handle_client_connection(socket_obj)