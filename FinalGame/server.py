import socket
import threading
import pickle
import random
import time

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# Pygame setup
import pygame
pygame.init()

# Game variables
score = {'player': 0}
moles = []

# Initialize the Pygame screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Whack-a-Mole Server")

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

# Function to handle a client connection
def handle_client(client_socket):
    global score, moles

    while True:
        try:
            # Generate moles randomly
            moles = [{'rect': pygame.Rect(random.randint(0, screen_width - 50), random.randint(0, screen_height - 50), 50, 50),
                      'active': True} for _ in range(random.randint(1, 3))]

            # Send moles to the client
            client_socket.send(pickle.dumps(moles))

            # Sleep for a short duration before sending new moles
            time.sleep(2)

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    print("Connection closed")
    client_socket.close()

# Accept client connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} accepted")

    # Start a new thread for each client
    threading.Thread(target=handle_client, args=(client_socket,)).start()
