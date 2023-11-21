import socket
import select


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host, port = "127.0.0.1", 9999


server.bind((host, port))
server.listen(5)



socket_objs = [server]

print("Bienvenue dans le chatroom !!!")


# Ajouter un dictionnaire pour stocker les noms associés aux sockets
client_noms = {}

def broadcast(server_socket, sender_socket, message):
    for socket_obj in socket_objs:
        if socket_obj != server_socket and socket_obj != sender_socket:
            try:
                socket_obj.send(f"{message}".encode('utf-8'))
            except:
                socket_objs.remove(socket_obj)


while True:
    list_lue, list_accee_Ecrit, exception = select.select(
        socket_objs, [], socket_objs)

    for socket_obj in list_lue:
        if socket_obj is server:

            client, address = server.accept()
            socket_objs.append(client)
            # Demander le nom au client
            client_name = client.recv(128).decode('utf-8')
            client_noms[client] = client_name

            print(f"Nouveau participant {client_name} connecte depuis {address}")
            broadcast(server, client, f"{client_name} a rejoint le chatroom.")
        else:
            try:
                donnees_recus = socket_obj.recv(128).decode('utf-8')

                if donnees_recus:
                    print(donnees_recus)
                    broadcast(server, socket_obj, donnees_recus)
            except ConnectionResetError:

                socket_objs.remove(socket_obj)
                print(client_noms[socket_obj] +" s'est deconnecte")
                broadcast(server, socket_obj, client_noms[socket_obj] + " s'est deconnecte.")
                print(f"{len(socket_objs) - 1} participants restants")

