import socket
import threading
import pickle

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Store connected clients
clients = []

# Game state
ball_pos = [400, 300]
paddle1_pos = [50, 250]
paddle2_pos = [750, 250]

# Ball speed
ball_speed = [5, 5]

# Broadcast message to all clients
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(pickle.dumps(message))
            except:
                # Remove disconnected client
                clients.remove(client)

# Handle client connections
def handle_client(client):
    global ball_pos, paddle1_pos, paddle2_pos
    while True:
        try:
            data = pickle.loads(client.recv(1024))
            paddle1_pos = data["paddle1_pos"]
            paddle2_pos = data["paddle2_pos"]
            broadcast({"ball_pos": ball_pos, "paddle1_pos": paddle1_pos, "paddle2_pos": paddle2_pos}, client)
        except:
            # Remove disconnected client
            clients.remove(client)
            break

# Accept and handle client connections
while True:
    client, address = server_socket.accept()
    clients.append(client)
    print(f"Connection established with {address}")
    
    # Start a new thread for each client
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
