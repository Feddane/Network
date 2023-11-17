import socket

client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = "127.0.0.1", 9999

#tentative de connexion au serveur
client.connect((host, port))

nom = input('Quel est votre nom ?')

#s'assurer que le code dans ce bloc est exécuté uniquement lorsque le script est exécuté directement et non lorsqu'il est importé en tant que module.
if __name__ == '__main__':
    while True:

        message = input(f"{nom} >")
        client.send(f"{nom} > {message}".encode("utf-8"))

