import socket
import threading
import random

def handle_client(client, user_name):
    num = random.randint(1, 20)
    print(f"Le nombre aléatoire est {num} pour {user_name}")

    turn = 0
    while turn <= 5:
        try:
            turn += 1
            data = int(client.recv(2048).decode())

            if data == num:
                client.send("Win".encode() + str(turn).encode())
                break
            elif data > num:
                if turn == 5:
                    client.send("Lost".encode() + str(turn).encode())
                    break
                else:
                    client.send("High".encode() + str(turn).encode())
            elif data < num:
                if turn == 5:
                    client.send("Lost".encode() + str(turn).encode())
                    break
                else:
                    client.send("Low".encode() + str(turn).encode())

        except ValueError:
            break

    print(f"Nombre de tours effectués pour {user_name}: {turn}")
    client.close()

def main():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("127.0.0.1", 8001))
    serveur.listen(5)  # Accepte jusqu'à 5 connexions simultanées

    print("Attente de connexions...")

    while True:
        client, (ip, port) = serveur.accept()
        user_name = client.recv(1024).decode()
        print(f"{user_name} s'est connecté depuis {ip}:{port}")

        # Crée un thread pour gérer le client actuel
        client_handler = threading.Thread(target=handle_client, args=(client, user_name))
        client_handler.start()

if __name__ == "__main__":
    main()
