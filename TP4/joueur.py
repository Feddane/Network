import socket

def get_user_choice():
    choice = input("Enter your choice (rock, paper, scissors) or type 'exit' to leave: ").lower()
    return choice

# Initialize client
host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

print("Bienvenue au jeu!")  # Welcome message

try:
    while True:
        user_choice = get_user_choice()
        client.send(user_choice.encode('utf-8'))

        if user_choice == 'exit':
            break
except KeyboardInterrupt:
    print("Game interrupted.")
finally:
    client.close()
