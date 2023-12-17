import socket       # Modules utilisés
import random

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Création du socket
serveur.bind(("127.0.0.1", 8001))  # Liaison du socket à l'adresse IP locale et au port 8000

while True:
    serveur.listen(1)   # Attente d'une connexion (1 connexion à la fois)
    (client, (ip, port)) = serveur.accept()   # Acceptation de la connexion
    print("Connecté")

    num = random.randint(1, 20)   # Génération d'un nombre aléatoire entre 1 et 20
    print("Le nombre aléatoire est ", num)
    turn = 0

    while turn <= 5:   # Logique du jeu
        try:
            turn += 1
            data = int(client.recv(2048).decode())   # Réception des données du client
            if int(data) == num:
                client.send("Win".encode() + str(turn).encode())   # Envoi du message "Win" et du nombre de tours
                break
            if int(data) > num:
                if turn == 5:
                    client.send("Lost".encode() + str(turn).encode())   # Envoi du message "Lost" et du nombre de tours
                    break
                else:
                    client.send("High".encode() + str(turn).encode())   # Envoi du message "High" et du nombre de tours
            if int(data) < num:
                if turn == 5:
                    client.send("Lost".encode() + str(turn).encode())   # Envoi du message "Lost" et du nombre de tours
                    break
                else:
                    client.send("Low".encode() + str(turn).encode())   # Envoi du message "Low" et du nombre de tours
        except ValueError:
            break

    print("Nombre de tours effectués ", turn)
