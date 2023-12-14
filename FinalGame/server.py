import socket
import threading
from tkinter import *
from tkinter import messagebox
import sys

# Configuration du serveur
host = '127.0.0.1'
port = 65535

# Initialisation du socket pour la communication réseau
conn, addr = None, None
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

# Initialisation de la fenêtre Tkinter
window = Tk()
window.title("Bienvenue Joueur 1 au jeu de Tic-Tac-Toe")
window.geometry("400x300")

# Création des étiquettes dans la fenêtre
lbl = Label(window, text="Jeu de Tic-Tac-Toe", font=('Helvetica', 15))
lbl.grid(row=0, column=0)
lbl = Label(window, text="Joueur 1: X", font=('Helvetica', 10))
lbl.grid(row=1, column=0)
lbl = Label(window, text="Joueur 2: O", font=('Helvetica', 10))
lbl.grid(row=2, column=0)

# Variables globales
cell = ''  # stocke la position du dernier coup joué.
turn = True  # indique si c'est au tour du serveur de jouer.

score_player1 = 0
score_player2 = 0


# Fonction pour recevoir les données du réseau
# Elle reçoit les données du client, décode le message, met à jour la variable cell et appelle la fonction update.
def recieveData():
    global cell
    global turn
    while True:
        data, addr = conn.recvfrom(1024)  # Boucle pour recevoir l'adresse et le message
        data2 = data.decode('utf-8')
        dataa = data2.split('-')
        cell = dataa[0]
        update()

        # Si le message est 'TonTour', elle définit turn sur True.
        if dataa[1] == 'TonTour':
            turn = True
            print(" Serveur tour = " + str(turn))


# Fonction pour mettre à jour l'interface graphique en fonction des données reçues
def update():
    if cell == 'A':
        clicked1()
    elif cell == 'B':
        clicked2()
    elif cell == 'C':
        clicked3()
    elif cell == 'D':
        clicked4()
    elif cell == 'E':
        clicked5()
    elif cell == 'F':
        clicked6()
    elif cell == 'G':
        clicked7()
    elif cell == 'H':
        clicked8()
    elif cell == 'I':
        clicked9()
    else:
        print("Aucun caractère correspondant détecté")


# Fonction pour créer un thread
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True  # démons sont des threads qui s'exécutent en arrière-plan et sont automatiquement tués lorsque le programme principal se termine.
    thread.start()


# Fonction pour attendre une connexion client
def waitingforconnection():
    print("Thread créé")
    global conn, addr
    try:
        conn, addr = server.accept()
        print("Client connected")
        recieveData()
    except OSError:
        print("Le client a fermé la connexion. Fin de la partie.")
        sys.exit()


# Création d'un thread pour attendre la connexion client
create_thread(waitingforconnection)

# Fonctions pour gérer les clics sur les boutons du jeu
# Ces fonctions envoient également des données au client via le réseau
def clicked1():
    global turn  # qui va jouer (serveur ou client)
    global cell
    if turn == True and btn1["text"] == " ":  # si c moi qui joue et si mon boutton est vide
        btn1["text"] = "X"  # serveur toujours joue avec X et le client avec O
        send_data = '{}-{}'.format('A', 'TonTour').encode()  # A, TonTour est le message que le serveur va envoyer au client
        conn.send(send_data)
        print(send_data)
        turn = False  # on stop la saisie du serveur
        check()
    # le client effectue un mouvement
    elif turn == False and btn1["text"] == " " and cell == 'A':
        btn1["text"] = "O"
        turn = True  # c'est le tour du serveur
        check()


def clicked2():
    global turn
    global cell
    if turn == True and btn2["text"] == " ":
        btn2["text"] = "X"
        send_data = '{}-{}'.format('B', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn2["text"] == " " and cell == 'B':
        btn2["text"] = "O"
        turn = True
        check()


def clicked3():
    global turn
    global cell
    if turn == True and btn3["text"] == " ":
        btn3["text"] = "X"
        send_data = '{}-{}'.format('C', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn3["text"] == " " and cell == 'C':
        btn3["text"] = "O"
        turn = True
        check()


def clicked4():
    global turn
    global cell
    if turn == True and btn4["text"] == " ":
        btn4["text"] = "X"
        send_data = '{}-{}'.format('D', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn4["text"] == " " and cell == 'D':
        btn4["text"] = "O"
        turn = True
        check()


def clicked5():
    global turn
    global cell
    if turn == True and btn5["text"] == " ":
        btn5["text"] = "X"
        send_data = '{}-{}'.format('E', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn5["text"] == " " and cell == 'E':
        btn5["text"] = "O"
        turn = True
        check()


def clicked6():
    global turn
    global cell
    if turn == True and btn6["text"] == " ":
        btn6["text"] = "X"
        send_data = '{}-{}'.format('F', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn6["text"] == " " and cell == 'F':
        btn6["text"] = "O"
        turn = True
        check()


def clicked7():
    global turn
    global cell
    if turn == True and btn7["text"] == " ":
        btn7["text"] = "X"
        send_data = '{}-{}'.format('G', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn7["text"] == " " and cell == 'G':
        btn7["text"] = "O"
        turn = True
        check()


def clicked8():
    global turn
    global cell
    if turn == True and btn8["text"] == " ":
        btn8["text"] = "X"
        send_data = '{}-{}'.format('H', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        check()
    elif turn == False and btn8["text"] == " " and cell == 'H':
        btn8["text"] = "O"
        turn = True
        check()


def clicked9():
    global turn
    global cell
    if turn == True and btn9["text"] == " ":
        btn9["text"] = "X"
        send_data = '{}-{}'.format('I', 'TonTour').encode()
        conn.send(send_data)
        print(send_data)
        turn = False
        print(" Server turn = " + str(turn))
        check()
    elif turn == False and btn9["text"] == " " and cell == 'I':
        btn9["text"] = "O"
        turn = True
        check()


flag = 1  # Elle est utilisée pour suivre le nombre total de coups joués dans la partie.

# Fonction pour vérifier s'il y a un gagnant ou une égalité
def check():  # check if a win case exists
    global flag
    b1 = btn1["text"]  # Ex: X ou O
    b2 = btn2["text"]
    b3 = btn3["text"]
    b4 = btn4["text"]
    b5 = btn5["text"]
    b6 = btn6["text"]
    b7 = btn7["text"]
    b8 = btn8["text"]
    b9 = btn9["text"]
    flag = flag + 1

    # Logique pour vérifier les différentes combinaisons gagnantes
    if b1 == b2 and b1 == b3 and b1 == "O" or b1 == b2 and b1 == b3 and b1 == "X":
        win(b1)  # x ou o
    if b4 == b5 and b4 == b6 and b4 == "O" or b4 == b5 and b4 == b6 and b4 == "X":
        win(b4)
    if b7 == b8 and b7 == b9 and b7 == "O" or b7 == b8 and b7 == b9 and b7 == "X":
        win(b7)
    if b1 == b4 and b1 == b7 and b1 == "O" or b1 == b4 and b1 == b7 and b1 == "X":
        win(b1)
    if b2 == b5 and b2 == b8 and b2 == "O" or b2 == b5 and b2 == b8 and b2 == "X":
        win(b2)
    if b3 == b6 and b3 == b9 and b3 == "O" or b3 == b6 and b3 == b9 and b3 == "X":
        win(b3)
    if b1 == b5 and b1 == b9 and b1 == "O" or b1 == b5 and b1 == b9 and b1 == "X":
        win(b1)
    if b7 == b5 and b7 == b3 and b7 == "O" or b7 == b5 and b7 == b3 and b7 == "X":
        win(b7)
    # si les 9 tours ont ete atteint car flag = 1
    if flag == 10:
        messagebox.showinfo("Égalité ", "Match nul !! Essayez à nouveau :)")
        window.destroy()


# Fonction pour afficher la boîte de dialogue lorsque le jeu est terminé
def win(player):
    global score_player1, score_player2
    ans = "Partie terminée " + player + " a gagné !"

    if player == 'X':
        score_player1 += 1
    elif player == 'O':
        score_player2 += 1

    ans += f"\n\nScore:\nJoueur 1 : {score_player1}\nJoueur 2: {score_player2}"

    messagebox.showinfo("Félicitations", ans)
    window.destroy()  # is used to close the program



# Création des boutons pour le jeu
btn1 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked1)
btn1.grid(column=1, row=1)

btn2 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked2)
btn2.grid(column=2, row=1)

btn3 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked3)
btn3.grid(column=3, row=1)

btn4 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked4)
btn4.grid(column=1, row=2)

btn5 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked5)
btn5.grid(column=2, row=2)

btn6 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked6)
btn6.grid(column=3, row=2)

btn7 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked7)
btn7.grid(column=1, row=3)

btn8 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked8)
btn8.grid(column=2, row=3)

btn9 = Button(window, text=" ", bg="white", fg="black", width=3, height=1, font=('Helvetica', 20), command=clicked9)
btn9.grid(column=3, row=3)

# Lancement de la boucle principale de l'interface graphique
window.mainloop()
