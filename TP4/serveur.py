import socket
import threading

# Fonction de diffusion du message à tous les clients
def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

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
            # Incrémenter le tour actuel
            current_round += 1

            determine_winner()
            reset_choices()

    # Afficher "Fin du jeu" lorsque le joueur quitte
    print("Fin du jeu")
    conn.close()



# Déterminer le vainqueur du tour
def determine_winner():
    global score_player1, score_player2, current_round
    choices_str = ', '.join(choices)

    if choices[0] == choices[1]:
        result_message = "C'est une egalite !"
        print(result_message)
    elif (choices[0] == 'pierre' and choices[1] == 'ciseaux') or \
         (choices[0] == 'papier' and choices[1] == 'pierre') or \
         (choices[0] == 'ciseaux' and choices[1] == 'papier'):
        result_message = f"{player_names[0]} gagne ! ({choices_str})"
        print(result_message)
        score_player1 += 1
    else:
        result_message = f"{player_names[1]} gagne ! ({choices_str})"
        print(result_message)
        score_player2 += 1

    #Afficher le score 
    score_message = f"\nScore pour le tour {current_round}:\n{player_names[0]}: {score_player1}\n{player_names[1]}: {score_player2}\n"
    print(score_message)

    # Envoyer le résultat et le score au client
    message = f"{result_message} \n{score_message}"
    broadcast(message)

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
