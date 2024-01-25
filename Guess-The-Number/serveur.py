import socket
import threading
import random

connected_clients = {}  # Dictionary to track connected clients

# Function to handle the client
def handle_client(client, username):
    # Generate a random number between 1 and 20 for the client
    num = random.randint(1, 20)
    print(f"The random number is {num} for {username}")

    turn = 0
    while turn <= 5:
        try:
            turn += 1
            # Receive data from the client and convert it to an integer
            data = int(client.recv(2048).decode())

            if data == num:
                # Send a message indicating that the client has won and the number of turns
                client.send("Won".encode() + str(turn).encode())
                break
            elif data > num:
                if turn == 5:
                    # Send a message indicating that the client has lost and the number of turns
                    client.send("Lost".encode() + str(turn).encode())
                    break
                else:
                    # Send a message indicating that the number is too high and the number of turns
                    client.send("TooHigh".encode() + str(turn).encode())
            elif data < num:
                if turn == 5:
                    # Send a message indicating that the client has lost and the number of turns
                    client.send("Lost".encode() + str(turn).encode())
                    break
                else:
                    # Send a message indicating that the number is too low and the number of turns
                    client.send("TooLow".encode() + str(turn).encode())

        except ValueError:
            break

    print(f"Number of turns for {username}: {turn}")
    disconnect_user(username)  # Call the function to handle disconnection
    client.close()

# Function to handle disconnection
def disconnect_user(username):
    if username in connected_clients:
        # Remove the client from the list of connected clients
        del connected_clients[username]
        print(f"{username} has disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8000))
    server.listen()

    print("Waiting for connections...")

    while True:
        client, (ip, port) = server.accept()
        username = client.recv(1024).decode()
        print(f"{username} has connected from {ip}:{port}")

        connected_clients[username] = client  # Add the client to the list of connected clients

        # Create a thread to handle the current client
        client_handler = threading.Thread(target=handle_client, args=(client, username))
        client_handler.start()

if __name__ == "__main__":
    main()
