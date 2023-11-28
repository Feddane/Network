import socket
import select
from random import randint
import threading

def gestion_client(client, address):
    jeu = ["pierre", "papier", "ciseaux"]
    score_joueur = 0
    score_ordinateur = 0
    
    print(f"Nouveau client connecté : {address}")

    while True:
        try:
            list_lue, _, _ = select.select([client], [], [], 1)

            if list_lue:
                donnees_recues = client.recv(128).decode('utf-8')
            else:
                continue

            if not donnees_recues:
                print(f"Le client {address} s'est déconnecté.")
                socket_objs.remove(client)  # Retirer la socket fermée de la liste
                break

            joueur = donnees_recues.strip().lower()

            if joueur == 'fin':
                print(f"Le client {address} a quitté la partie.")
                socket_objs.remove(client)  # Retirer la socket fermée de la liste

                # Envoyer le score final avant de fermer la connexion
                score_final_message = f"Fin de la partie!\nScore Final - Joueur: {score_joueur}, Ordinateur: {score_ordinateur}"
                client.send(score_final_message.encode("utf-8"))
                
                # Sortir de la boucle pour fermer la connexion
                break
            elif joueur in jeu:
                # L'ordinateur fait un choix aléatoire
                ordinateur = jeu[randint(0, 2)]
                
                # Logique du jeu
                if joueur == ordinateur:
                    resultat = "Egalité!"
                elif (joueur == "pierre" and ordinateur == "ciseaux") or \
                    (joueur == "papier" and ordinateur == "pierre") or \
                    (joueur == "ciseaux" and ordinateur == "papier"):
                    resultat = f"Gagné! {joueur} bat {ordinateur}"
                    score_joueur += 1
                else:
                    resultat = f"Perdu! {ordinateur} bat {joueur}"
                    score_ordinateur += 1

                # Pas besoin d'afficher le score ici

                # Envoyer le résultat du jeu au client
                client.send(resultat.encode("utf-8"))
            else:
                print("Choix non valide. Veuillez choisir entre pierre, papier et ciseaux.")
                client.send("Choix non valide. Veuillez choisir entre pierre, papier et ciseaux.".encode("utf-8"))

        except Exception as e:
            print(f"Erreur lors de la gestion du client {address} : {e}")
            socket_objs.remove(client)
            break

    client.close()



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = "127.0.0.1", 9999

server.bind((host, port))
server.listen(4)

client_connected = True
socket_objs = [server]  # Ajouter le serveur à la liste

print("Bienvenue dans le jeu de pierre-papier-ciseaux!")

while client_connected:
    list_lue, _, _ = select.select(socket_objs, [], socket_objs)

    for socket_obj in list_lue:
        if socket_obj is server:
            client, address = server.accept()
            socket_objs.append(client)
            threading.Thread(target=gestion_client, args=(client, address)).start()
        else:
            continue
