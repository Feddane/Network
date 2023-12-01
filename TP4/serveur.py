import socket
import threading

def handle_client(conn, player):
    global current_round

    player_name = conn.recv(1024).decode('utf-8')
    print(f"{player_name} joined the game.")

    # Add player name to the list of player names
    player_names.append(player_name)


    while True:
        choice = conn.recv(1024).decode('utf-8')
        if not choice or choice.lower() == 'exit':
            print(f"{player_name} has left the game.")
            break


        print(f"{player_name} choice: {choice}")
        choices[player - 1] = choice


        # Check if both players have made their choices
        if all(choices):
            determine_winner()
            reset_choices()

            # Increment the current round
            current_round += 1
            print(f"\nScore for round {current_round}:")
            print(f"{player_names[0]}: {score_player1}")
            print(f"{player_names[1]}: {score_player2}\n")

            # Send the result to both clients
            result_message = f"Round {current_round} result - {player_names[0]}: {score_player1}, {player_names[1]}: {score_player2}"
            for client in clients:
                client.send(result_message.encode('utf-8'))


    # Add the following lines after the while loop to print "Game ended" when the player exits
    print("Game ended")
    conn.close()


def determine_winner():
    global score_player1, score_player2
    choices_str = ', '.join(choices)
    if choices[0] == choices[1]:
        print("It's a tie!")
    elif (choices[0] == 'rock' and choices[1] == 'scissors') or \
         (choices[0] == 'paper' and choices[1] == 'rock') or \
         (choices[0] == 'scissors' and choices[1] == 'paper'):
        print(f"{player_names[0]} wins! ({choices_str})")
        score_player1 += 1
    else:
        print(f"{player_names[1]} wins! ({choices_str})")
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

player_names = [] # Initialize an empty list to store player names


while True:
    conn, addr = server.accept()
    player_count += 1
    print(f"Connection from {addr}")
    
    clients.append(conn)

    # Start a new thread to handle the current client
    threading.Thread(target=handle_client, args=(conn, player_count)).start()