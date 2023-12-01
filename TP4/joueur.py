import socket

def get_user_name():
    while True:
        name = input("Quel est votre nom? ")
        if name:
            return name
        else:
            print("Le nom ne peut pas être vide.")

def get_user_choice():
    while True:
        choice = input("Enter your choice (rock, paper, scissors) or type 'exit' to leave: ").lower()
        if choice in ['rock', 'paper', 'scissors', 'exit']:
            return choice
        else:
            print("Votre choix n'est pas correct, vérifiez l'orthographe!")

# Initialize client
host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

print("Bienvenue au jeu!")  # Welcome message
user_name = get_user_name()
client.send(user_name.encode('utf-8'))

try:
    while True:
        user_choice = get_user_choice()
        client.send(user_choice.encode('utf-8'))

        if user_choice == 'exit':
            break

        # Receive and display the result after each round
        result_message = client.recv(1024).decode('utf-8')
        print(result_message)

except KeyboardInterrupt:
    print("Game interrupted.")
finally:
    client.close()
