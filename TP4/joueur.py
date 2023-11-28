import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = "127.0.0.1", 9999

# tentative de connexion au serveur
client.connect((host, port))

nom = input('Quel est votre nom ? ')

print("Bienvenue dans le jeu de pierre-papier-ciseaux!")
print("pierre, papier, ciseaux? ou tapez fin pour arrêter le jeu!\n")

# s'assurer que le code dans ce bloc est exécuté uniquement lorsque le script est exécuté directement et non lorsqu'il est importé en tant que module.
if __name__ == '__main__':
    while True:
        message = input(f"{nom} > ")
        client.send(message.encode("utf-8"))

        # Recevoir la réponse du serveur (résultat du jeu)
        reponse = client.recv(128).decode('utf-8')

        if reponse.lower() == 'fin':
            print("Partie terminée.")
            break

        print(f"{nom} > {reponse}")

    client.close()
