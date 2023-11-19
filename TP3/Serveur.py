import socket
import select


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host, port = "127.0.0.1", 9999


server.bind((host, port))
server.listen(5)


socket_objs = [server]

print("Bienvenue dans le chatroom !!!")


def broadcast(server_socket, sender_socket, message):
    for socket_obj in socket_objs:

        if  socket_obj != server_socket and socket_obj != sender_socket:
            try:
                socket_obj.send(message.encode('utf-8'))
            except:

                socket_objs.remove(socket_obj)

while True:
    list_lue, list_accee_Ecrit, exception = select.select(
        socket_objs, [], socket_objs)

    for socket_obj in list_lue:
        if socket_obj is server:

            client, address = server.accept()
            socket_objs.append(client)
            print(f"Nouveau participant connecte depuis {address}")
            broadcast(server, client, f"{address} a rejoint le chatroom.")
        else:
            try:
                donnees_recus = socket_obj.recv(128).decode('utf-8')

                if donnees_recus:
                    print(donnees_recus)
                    broadcast(server, socket_obj, donnees_recus)
            except ConnectionResetError:

                socket_objs.remove(socket_obj)
                print(f"Un participant est deconnecte")
                broadcast(server, socket_obj, "Un participant s'est deconnecte.")
                print(f"{len(socket_objs) - 1} participants restants")

