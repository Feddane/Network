import socket
import threading
import random

clients_connectes = {}  # Dictionnaire pour suivre les clients connectés

def handle_client(client, nom_utilisateur):
    # Génère un nombre aléatoire entre 1 et 20 pour le client
    num = random.randint(1, 20)
    print(f"Le nombre aléatoire est {num} pour {nom_utilisateur}")

    turn = 0
    while turn <= 5:
        try:
            turn += 1
            # Reçoit les données du client et les convertit en entier
            donnees = int(client.recv(2048).decode())

            if donnees == num:
                # Envoie un message indiquant que le client a gagné et le nombre de tours
                client.send("Win".encode() + str(turn).encode())
                break
            elif donnees > num:
                if turn == 5:
                    # Envoie un message indiquant que le client a perdu et le nombre de tours
                    client.send("Lost".encode() + str(turn).encode())
                    break
                else:
                    # Envoie un message indiquant que le nombre est trop élevé et le nombre de tours
                    client.send("High".encode() + str(turn).encode())
            elif donnees < num:
                if turn == 5:
                    # Envoie un message indiquant que le client a perdu et le nombre de tours
                    client.send("Lost".encode() + str(turn).encode())
                    break
                else:
                    # Envoie un message indiquant que le nombre est trop bas et le nombre de tours
                    client.send("Low".encode() + str(turn).encode())

        except ValueError:
            break

    print(f"Nombre de tours effectués pour {nom_utilisateur}: {turn}")
    disconnect_user(nom_utilisateur)  # Appel de la fonction pour gérer la déconnexion
    client.close()

def disconnect_user(nom_utilisateur):
    if nom_utilisateur in clients_connectes:
        # Supprime le client de la liste des clients connectés
        del clients_connectes[nom_utilisateur]
        print(f"{nom_utilisateur} s'est déconnecté.")

def main():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.bind(("127.0.0.1", 8001))
    serveur.listen(5)  # Accepte jusqu'à 5 connexions simultanées

    print("Attente de connexions...")

    while True:
        client, (ip, port) = serveur.accept()
        nom_utilisateur = client.recv(1024).decode()
        print(f"{nom_utilisateur} s'est connecté depuis {ip}:{port}")

        clients_connectes[nom_utilisateur] = client  # Ajoute le client à la liste des clients connectés

        # Crée un thread pour gérer le client actuel
        client_handler = threading.Thread(target=handle_client, args=(client, nom_utilisateur))
        client_handler.start()

if __name__ == "__main__":
    main()
