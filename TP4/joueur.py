import socket

# Fonction pour obtenir le nom d'utilisateur
def get_user_name():
    while True:
        name = input("Quel est votre nom ? ")
        if name:
            return name
        else:
            print("Le nom ne peut pas être vide.")

# Fonction pour obtenir le choix de l'utilisateur
def get_user_choice():
    while True:
        choice = input("Entrez votre choix (pierre, papier, ciseaux) ou tapez 'exit' pour quitter : ").lower()
        if choice in ['pierre', 'papier', 'ciseaux', 'exit']:
            return choice
        else:
            print("Votre choix n'est pas correct, vérifiez l'orthographe !")

# Définir l'hôte (adresse IP) et le port sur lequel le client se connectera
host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecte au serveur
client.connect((host, port))

print("Bienvenue au jeu !")  # Message de bienvenue
user_name = get_user_name()
client.send(user_name.encode('utf-8'))

try:
    while True:
        user_choice = get_user_choice()
        client.send(user_choice.encode('utf-8'))

        if user_choice == 'exit':
            break

        # Recevoir et afficher le résultat après chaque tour
        message = client.recv(1024).decode('utf-8')
        print(message)

except KeyboardInterrupt:
    print("Jeu interrompu.")
finally:
    client.close()
