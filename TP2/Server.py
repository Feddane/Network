import socket

import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = "127.0.0.1", 9999

server.bind((host, port))
server.listen(4)

client_connected = True
socket_objs = [server]

print("Welcome to the chat !!!")

while client_connected:
    list_lue, list_accee_Ecrit, exception = select.select(
        socket_objs, [], socket_objs)

    # list_lue = le client en attente ou le socket connecté, on cree une memoire tompon qui contient plusieurs clients et qui passent un par un

    for socket_obj in list_lue:

        if socket_obj is server:
            client, address = server.accept()
            socket_objs.append(client)  # ajouter le client connecté
        else:
            # il y'a un client qui a envoyer des messages au serveur
            # on essaie de recuperer le message envoyer au serveur
            donnees_recus = socket_obj.recv(128).decode('utf-8')

            # si les donnees ne sont pas vide/ client connecte
            if donnees_recus:
                print(donnees_recus)

            #un client est deconnecte
            else:
                socket_objs.remove(socket_obj)
                print("1 participant est deconnecte")
                print(f"{len(socket_objs) -1} participants restants")
