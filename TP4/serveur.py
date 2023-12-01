import socket
import threading

def handle_client(conn, player):
    global current_round, game_ended
    while True:
        choice = conn.recv(1024).decode('utf-8')
        if not choice or choice.lower() == 'exit':
            print(f"Player {player} has left the game.")
            break
        print(f"Player {player} choice: {choice}")
        choices[player - 1] = choice

        # Check if both players have made their choices
        if all(choices):
            determine_winner()
            reset_choices()

            # Increment the current round
            current_round += 1
            print(f"\nScore for round {current_round}:")
            print(f"Player 1: {score_player1}")
            print(f"Player 2: {score_player2}\n")

    conn.close()

    # # If the game hasn't ended and a player exits, end the game and display the number of rounds played
    # if not game_ended:
    #     game_ended = True
    #     print(f"\nGame ended after {current_round} rounds.")

def determine_winner():
    global score_player1, score_player2
    choices_str = ', '.join(choices)
    if choices[0] == choices[1]:
        print("It's a tie!")
    elif (choices[0] == 'rock' and choices[1] == 'scissors') or \
         (choices[0] == 'paper' and choices[1] == 'rock') or \
         (choices[0] == 'scissors' and choices[1] == 'paper'):
        print(f"Player 1 wins! ({choices_str})")
        score_player1 += 1
    else:
        print(f"Player 2 wins! ({choices_str})")
        score_player2 += 1

def reset_choices():
    global choices
    choices = [None, None]

# Initialize server
host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print("Bienvenue au jeu!")  # Welcome message

print(f"Server listening on {host}:{port}")

# Accept connections from clients
player_count = 0
clients = []

# Initialize game state
choices = [None, None]
score_player1 = 0
score_player2 = 0

# Track the current round and game status
current_round = 0
game_ended = False

while True:
    conn, addr = server.accept()
    player_count += 1
    print(f"Connection from {addr}")
    print(f"Player {player_count} joined the game.")
    clients.append(conn)

    # Start a new thread to handle the current client
    threading.Thread(target=handle_client, args=(conn, player_count)).start()