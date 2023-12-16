from tkinter import *   # Importation des modules nécessaires
import socket


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Fonction du bouton de sortie (ferme la fenêtre actuelle et réaffiche la fenêtre principale)
def exit_b(window):
    window.destroy()
    main_win.deiconify()
    b_new_game["state"] = "normal"
    b_score["state"] = "normal"

# Fenêtre d'un nouveau jeu / Connexion au socket
def new_game():
    # Fonction de réinitialisation
    def reset():
        game_win.destroy()
        new_game()

    # Winner function updates Score Board
    def winner(_server_data):
        canvas_game.itemconfig(server_print, text="Vous avez gagné")
        turn = _server_data[-1]
        canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
        b_submit.place_forget()

        b_new_game_l = Button(game_win, text="Nouveau Jeu", height=2, width=26, bg="white", relief="raised",
                              activebackground="#eddbd6", state=NORMAL, font="Forte 16", command=reset)
        b_new_game_l.place(x=400, y=400, anchor="center")
        place_score = user_name+" a gagné en "+turn+" coups\n"
        f = open("scoreBoard.txt", "a")
        f.write(place_score)
        f.close()

    # Fonction responsable de la session de socket
    def send_to_server():
        user_data = user_entry.get()   # Sauvegarde du champ d'entrée dans une variable ex:15
        tcpSocket.send(user_data.encode())   # Envoi au serveur envoi 15 au serveur
        server_data = tcpSocket.recv(2048).decode()   # Réception du serveur
        user_entry.delete(0, END)   # Effacer le champ d'entrée apres avoir envoyer la donnee au serveur (15)

        if "Lost" in server_data:   # Scénario où le joueur a perdu
            canvas_game.itemconfig(server_print, text="Vous avez perdu")
            b_submit.place_forget()   # Désactiver le bouton soumettre

            b_new_game_l = Button(game_win, text="Nouveau Jeu", height=2, width=26, bg="white", relief="raised",
                                  activebackground="#eddbd6", state=NORMAL, font="Forte 16", command=reset)

            b_new_game_l.place(x=400, y=400, anchor="center")
        elif "Win" in server_data:   # Nombre correct deviné
            winner(server_data)
        elif "High" in server_data:   # Nombre deviné trop élevé
            canvas_game.itemconfig(server_print, text="Trop élevé")
            turn = server_data[-1]  #le nombre de tour diminue
            canvas_game.itemconfig(attempt, text=("Essai : " + turn))
        elif "Low" in server_data:   # Nombre deviné trop bas
            canvas_game.itemconfig(server_print, text="Trop bas")
            turn = server_data[-1]
            canvas_game.itemconfig(attempt, text=("Essai : " + turn))
        else:
            canvas_game.itemconfig(server_print, text=server_data)

    #desactiver au debut du jeu pour l'utilisateur ne commence un nouveau jeu ou ne consulte le score pendant que le jeu est en cours
    b_new_game["state"] = "disable"   # Désactiver le bouton du menu principal
    b_score["state"] = "disable"   # Désactiver le bouton du menu principal

    #game_window
    game_win = Toplevel(main_win)
    game_win.geometry("800x600")
    game_win.resizable(0, 0)
    game_win.title("Jeu")
    center_window(game_win)
    canvas_game = Canvas(game_win, width=640, height=480)
    canvas_game.pack(fill="both", expand=True)
    canvas_game.create_image(0, 0, image=bg_game, anchor="nw")

    #rectangle
    canvas_game.create_rectangle(50, 120, 750, 450, fill="#d8d1ca", outline='black')

    canvas_game.create_text(400, 50, text="Devinez le nombre", fill="black", font="Forte 38", justify="center",
                            anchor="n")
    attempt = canvas_game.create_text(60, 130, text="Essai : 1", fill="#8f736c", font="Forte 18", justify="center",
                                      anchor="nw")

    canvas_game.create_text(60, 160, text=("Joueur : " + user_name), fill="#8f736c", font="Forte 18", anchor="nw")

    server_print = canvas_game.create_text(400, 180, text="Devinez le nombre entre\n1 et 20", fill="black",
                                           font="Forte 34", justify="center", anchor="n")

    user_entry = Entry(game_win, width=4, font="Forte 26 bold", justify="center", bg="white")
    canvas_game.create_window(400, 300, window=user_entry)

    b_submit = Button(game_win, text="Soumettre", height=2, width=26, bg="white", relief="raised",
                      activebackground="#eddbd6", state=NORMAL, font="Forte 16", command=send_to_server)

    b_submit.place(x=400, y=400, anchor="center")
    b_submit.bind("<Enter>", hover_in)
    b_submit.bind("<Leave>", hover_out)

    b_exit_score = Button(game_win, text="Quitter", height=2, width=26, bg="white", relief="raised",
                          activebackground="#eddbd6", command=lambda: exit_b(game_win), state=NORMAL, font="Forte 16")

    b_exit_score.place(x=400, y=530, anchor="center")
    b_exit_score.bind("<Enter>", hover_in)
    b_exit_score.bind("<Leave>", hover_out)

    #Definir socket client
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.connect(("127.0.0.1", 8001))

# Fenêtre du tableau des scores
def score_board():
    main_win.iconify()

    f = open("scoreBoard.txt", "r")
    scoreList = f.read()
    f.close()
    score_window = Toplevel(main_win)
    score_window.title("Score")
    center_window(score_window)
    score_window.geometry("480x640")
    score_window.resizable(0, 0)
    canvas_score = Canvas(score_window, width=480, height=640)
    canvas_score.pack(fill="both", expand=True)
    canvas_score.create_image(0, 0, image=bg_score, anchor="nw")

    canvas_score.create_text(240, 100, text="Tableau des Scores", fill="black", font="Forte 30 bold",
                             justify="center")
    canvas_score.create_text(240, 240, text=scoreList, fill="black", font="Forte 18", justify="center", anchor="n")
    b_exit_score = Button(score_window, text="Quitter", height=2, width=26, bg="white", relief="raised",
                          activebackground="#eddbd6", command=lambda: exit_b(score_window), state=NORMAL, font="Forte 16")

    b_exit_score.place(x=240, y=580, anchor="center")
    b_exit_score.bind("<Enter>", hover_in)
    b_exit_score.bind("<Leave>", hover_out)

# Fenêtre de connexion / Entrer le nom
def login():
    main_win.iconify()

    def start_b():
        global user_name
        user_name = enter_name.get()
        print(user_name)
        login_window.destroy()
        new_game()

    login_window = Toplevel(main_win)
    login_window.title("Connexion")
    login_window.geometry("400x250")
    login_window.resizable(0, 0)
    center_window(login_window)
    canvas_login = Canvas(login_window, width=400, height=250)
    canvas_login.pack(fill="both", expand=True)
    canvas_login.create_image(0, 0, image=bg_login, anchor="nw")

    canvas_login.create_text(200, 40, text="Entrez votre nom", fill="black", font="Forte 26 bold", justify="center")
    enter_name = Entry(canvas_login, width=16, font="Forte 26 bold", justify="center", bg="white")
    canvas_login.create_window(200, 100, window=enter_name)

    b_start = Button(login_window, text="Commencer", height=1, width=20, bg="white", relief="raised",
                     activebackground="#eddbd6", command=start_b, state=NORMAL, font="Forte 16")
    b_exit_login = Button(login_window, text="Quitter", height=1, width=20, bg="white", relief="raised",
                          activebackground="#eddbd6", command=lambda: exit_b(login_window),
                          state=NORMAL, font="Forte 16")

    b_start.place(x=200, y=170, anchor="center")
    b_start.bind("<Enter>", hover_in)
    b_start.bind("<Leave>", hover_out)

    b_exit_login.place(x=200, y=220, anchor="center")
    b_exit_login.bind("<Enter>", hover_in)
    b_exit_login.bind("<Leave>", hover_out)

def hover_in(e):
    e.widget["background"] = "#eddbd6"

def hover_out(e):
    e.widget["background"] = "white"

#main window
main_win = Tk()
main_win.geometry("640x480")
main_win.resizable(0, 0)
main_win.title("Bienvenue au Jeu!")
center_window(main_win)

user_name = ""
bg_main = PhotoImage(file="images/menu.png")
bg_score = PhotoImage(file="images/score.png")
bg_login = PhotoImage(file="images/login.png")
bg_game = PhotoImage(file="images/game.png")

canvas_main = Canvas(main_win, width=640, height=480)
canvas_main.pack(fill="both", expand=True)
canvas_main.create_image(0, 0, image=bg_main, anchor="nw")


canvas_main.create_text(320, 80, text="Devinez le Nombre", fill="black", font="Forte 30 bold", justify="center",
                        anchor="n")

#les boutons de main window
b_new_game = Button(canvas_main, text="Nouveau Jeu", height=2, width=26, bg="white", fg="black", relief="raised",
                    activebackground="#eddbd6", command=login, state=NORMAL, font="Forte 16")
b_score = Button(canvas_main, text="Score", height=2, width=26, bg="white", fg="black", relief="raised",
                 activebackground="#eddbd6", command=score_board, state=NORMAL, font="Forte 16")
b_exit = Button(canvas_main, text="Quitter", height=2, width=26, bg="white", fg="black", relief="raised",
                activebackground="#eddbd6", command=main_win.destroy, state=NORMAL, font="Forte 16")



b_new_game.place(x=320, y=220, anchor="center")
b_new_game.bind("<Enter>", hover_in)
b_new_game.bind("<Leave>", hover_out)

b_score.place(x=320, y=290, anchor="center")
b_score.bind("<Enter>", hover_in)
b_score.bind("<Leave>", hover_out)

b_exit.place(x=320, y=380, anchor="center")
b_exit.bind("<Enter>", hover_in)
b_exit.bind("<Leave>", hover_out)

main_win.mainloop()

#item_config == mettre a jour le texte afficher
#main_win.iconify() ==  minimiser la fenêtre principale, c'est-à-dire pour la réduire à une icône dans la barre des tâches (ou la barre des applications, selon le système d'exploitation).