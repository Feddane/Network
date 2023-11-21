import socket
import threading
import  os


def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(128).decode('utf-8')
            if not message:
                break
            print(message)
    except Exception as e:
        print(f"Erreur de réception : {e}")
    finally:
        client_socket.close()
        print("La connexion au serveur a été fermée.")
        os._exit(0)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host, port = "127.0.0.1", 9999


client.connect((host, port))


nom = input('Quel est votre nom ? ')
client.send(nom.encode('utf-8'))


client.send(f"{nom} a rejoint le chatroom.".encode('utf-8'))


thread_receive = threading.Thread(target=receive_messages, args=(client,))
thread_receive.start()


while True:
    message = input(f"{nom} > ")
    client.send(f"{nom} > {message}".encode('utf-8'))



