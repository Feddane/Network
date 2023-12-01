import socket
import threading

def handle_client(conn, player):
    global current_round

    # Recevoir le nom du joueur du client
    player_name = conn.recv(1024).decode('utf-8')
    print(f"{player_name} a rejoint le jeu.")  # Afficher que le joueur a rejoint le jeu

    # Ajouter le nom du joueur à la liste des noms de joueurs
    player_names.append(player_name)

    while True:
        # Recevoir le choix du joueur du client
        choice = conn.recv(1024).decode('utf-8')
        if not choice or choice.lower() == 'exit':
            print(f"{player_name} a quitte le jeu.")  # Afficher que le joueur a quitté le jeu
            break

        print(f"choix de {player_name}: {choice}")

        # Enregistrer le choix du joueur
        choices[player - 1] = choice

        # Vérifier si les deux joueurs ont fait leur choix
        if all(choices):
            determine_winner()
            reset_choices()

            # Incrémenter le tour actuel
            current_round += 1
            print(f"\nScore pour le tour {current_round}:")
            print(f"{player_names[0]}: {score_player1}")
            print(f"{player_names[1]}: {score_player2}\n")

            # Envoyer le résultat aux deux clients
            result_message = f"Résultat du tour {current_round} - {player_names[0]}: {score_player1}, {player_names[1]}: {score_player2}"
            for client in clients:
                client.send(result_message.encode('utf-8'))

    # Ajouter les lignes suivantes après la boucle while pour afficher "Fin du jeu" lorsque le joueur quitte
    print("Fin du jeu")
    conn.close()

# Déterminer le vainqueur du tour
def determine_winner():
    global score_player1, score_player2
    choices_str = ', '.join(choices)
    if choices[0] == choices[1]:
        print("C'est une egalite !")
    elif (choices[0] == 'rock' and choices[1] == 'scissors') or \
         (choices[0] == 'paper' and choices[1] == 'rock') or \
         (choices[0] == 'scissors' and choices[1] == 'paper'):
        print(f"{player_names[0]} gagne ! ({choices_str})")
        score_player1 += 1
    else:
        print(f"{player_names[1]} gagne ! ({choices_str})")
        score_player2 += 1

# Réinitialiser les choix des joueurs
def reset_choices():
    global choices
    choices = [None, None]

# Initialiser le serveur
host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print("Bienvenue au jeu !")  # Message de bienvenue

print(f"Serveur en ecoute sur {host}:{port}")

# Accepter les connexions des clients
player_count = 0
clients = []

# Initialiser l'état du jeu
choices = [None, None]
score_player1 = 0
score_player2 = 0

# Suivre le tour actuel et l'état du jeu
current_round = 0

player_names = []  # Initialiser une liste vide pour stocker les noms des joueurs

while True:
    conn, addr = server.accept()
    player_count += 1
    print(f"Connexion depuis {addr}")

    clients.append(conn)

    # Démarrer un nouveau thread pour gérer le client actuel
    threading.Thread(target=handle_client, args=(conn, player_count)).start()
