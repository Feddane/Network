import socket
import threading
import random
import time

# Server Constants
HOST = '127.0.0.1'
PORT = 5555

# Game Constants
MOLE_APPEAR_TIME = 2  # in seconds
GAME_DURATION = 30  # in seconds

# Server variables
moles = []
last_mole_time = 0
scoreboard = {}

def handle_client(client, client_address, client_id):
    global moles, last_mole_time, scoreboard

    print(f"[*] Accepted connection from {client_address}")

    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break

            if data == "whack":
                current_time = time.time()
                if current_time - last_mole_time > MOLE_APPEAR_TIME:
                    moles.pop(0) if moles else None  # Whack the mole if there's one, else do nothing
                    last_mole_time = current_time

                    if client_id not in scoreboard:
                        scoreboard[client_id] = 1
                    else:
                        scoreboard[client_id] += 1

        except Exception as e:
            print(f"Error with client {client_id}: {e}")
            break

    print(f"[*] Connection from {client_address} closed")
    client.close()

def generate_mole():
    x, y = random.randint(50, 550), random.randint(50, 350)
    return x, y

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[*] Server is listening on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        client_id = random.randint(1, 1000)

        # Initialize client's score
        scoreboard[client_id] = 0

        # Generate a mole for the client
        moles.append(generate_mole())

        # Send the mole coordinates and client ID to the client
        client.send(f"{moles[0][0]},{moles[0][1]},{client_id}".encode('utf-8'))

        # Start a thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client, address, client_id))
        client_handler.start()

if __name__ == "__main__":
    start_server()
