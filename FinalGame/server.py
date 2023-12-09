import socket
import threading
import random
import time

def handle_client(conn, player, mole_callback):
    global current_round, score_player1, score_player2

    # Receive the player's name
    player_name = conn.recv(1024).decode('utf-8')
    print(f"{player_name} has joined the game.")

    while True:
        # Whack-a-Mole game logic
        time.sleep(2)  # Wait for 2 seconds before creating a new mole

        mole_x = random.randint(50, 750)
        mole_y = random.randint(50, 550)

        mole_callback((mole_x, mole_y))

        # Handle player's whack (not included in this response for brevity)
        # You need to implement the logic to handle the player's whack

    # Close the connection when the player leaves
    print(f"{player_name} has left the game.")
    conn.close()

# Server initialization code
host = '127.0.0.1'
port = 12347

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

print("Welcome to the Whack-a-Mole game!")
print(f"Server listening on {host}:{port}")

# Initialize game state variables
player_names = []
current_round = 0
score_player1 = 0
score_player2 = 0

# Create a list to store mole positions
mole_positions = []

def mole_callback(position):
    mole_positions.append(position)


# Initialize a variable to control the game state
game_running = True

def send_mole_positions():
    global game_running
    while game_running:
        time.sleep(5)  # Wait for 5 seconds before sending mole positions
        for conn in clients:
            mole_x = random.randint(50, 750)
            mole_y = random.randint(50, 550)
            message = f"MOLE {mole_x} {mole_y}"
            conn.send(message.encode('utf-8'))

    # Game over message
    for conn in clients:
        conn.send("GAME_OVER".encode('utf-8'))

# Start a separate thread to send mole positions to clients
threading.Thread(target=send_mole_positions).start()

# List to store client connections
clients = []

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, len(clients), mole_callback)).start()
