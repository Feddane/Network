from tkinter import *
import socket
import threading

# Function to center windows
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Function of the exit button (closes the current window and displays the main window again)
def exit_b(window):
    window.destroy()
    main_win.deiconify()
    b_new_game["state"] = "normal"
    b_score["state"] = "normal"

# Window for a new game / Connection to the socket
def new_game():
    # Reset function
    def reset():
        game_win.destroy()
        new_game()

    # Winner function updates Score Board
    def winner(_server_data):
        canvas_game.itemconfig(server_print, text="You won")
        turn = _server_data[-1]
        canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
        b_submit.place_forget()

        b_new_game_l = Button(game_win, text="New Game", height=2, width=26, bg="white", relief="raised",
                              activebackground="#eddbd6", state=NORMAL, font="Forte 16", command=reset)
        b_new_game_l.place(x=400, y=400, anchor="center")

        place_score = user_name + " won in " + turn + " attempts\n"
        f = open("scoreBoard.txt", "a")
        f.write(place_score)
        f.close()

    # Function responsible for the socket session
    def send_to_server():
        def communication_thread():
            user_data = user_entry.get()
            try:
                user_data = int(user_data)
                if 1 <= user_data <= 20:
                    client.send(str(user_data).encode())
                    server_data = client.recv(2048).decode()
                    user_entry.delete(0, END)

                    if "Lost" in server_data:
                        canvas_game.itemconfig(server_print, text="You lost")
                        b_submit.place_forget()
                        b_new_game_l = Button(game_win, text="New Game", height=2, width=26, bg="white",
                                            relief="raised", activebackground="#eddbd6", state=NORMAL,
                                            font="Forte 16", command=reset)
                        b_new_game_l.place(x=400, y=400, anchor="center")

                    elif "Won" in server_data:
                        winner(server_data)
                    elif "TooHigh" in server_data:
                        canvas_game.itemconfig(server_print, text="Too high")
                        turn = server_data[-1]
                        canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
                    elif "TooLow" in server_data:
                        canvas_game.itemconfig(server_print, text="Too low")
                        turn = server_data[-1]
                        canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
                    else:
                        canvas_game.itemconfig(server_print, text=server_data)
                else:
                    # Display a message if the number is not between 1 and 20
                    canvas_game.itemconfig(server_print, text="Enter a number between 1 and 20")
            except ValueError:
                # Display a message if the input is not an integer
                canvas_game.itemconfig(server_print, text="Enter an integer between 1 and 20")

        threading.Thread(target=communication_thread).start()

    # Disable at the beginning of the game so the user doesn't start a new game or check the score while the game is in progress
    b_new_game["state"] = "disable"   # Disable the button from the main menu
    b_score["state"] = "disable"   # Disable the button from the main menu

    # Creating the game window
    game_win = Toplevel(main_win)
    game_win.geometry("800x600")
    game_win.resizable(0, 0)
    game_win.title("Game")
    center_window(game_win)
    canvas_game = Canvas(game_win, width=640, height=480)
    canvas_game.pack(fill="both", expand=True)
    canvas_game.create_image(0, 0, image=bg_game, anchor="nw")

    # Rectangle
    canvas_game.create_rectangle(50, 120, 750, 450, fill="#d8d1ca", outline='black')

    canvas_game.create_text(400, 50, text="Guess the Number", fill="black", font="Forte 38", justify="center",
                            anchor="n")
    attempt = canvas_game.create_text(60, 130, text="Attempt: 1", fill="#8f736c", font="Forte 18", justify="center",
                                      anchor="nw")

    canvas_game.create_text(60, 160, text=("Player: " + user_name), fill="#8f736c", font="Forte 18", anchor="nw")

    server_print = canvas_game.create_text(400, 180, text="Guess the number between\n1 and 20", fill="black",
                                           font="Forte 30", justify="center", anchor="n")

    user_entry = Entry(game_win, width=4, font="Forte 26 bold", justify="center", bg="white")
    canvas_game.create_window(400, 300, window=user_entry)

    b_submit = Button(game_win, text="Submit", height=2, width=26, bg="white", relief="raised",
                      activebackground="#eddbd6", state=NORMAL, font="Forte 16", command=send_to_server)

    b_submit.place(x=400, y=400, anchor="center")
    b_submit.bind("<Enter>", hover_in)
    b_submit.bind("<Leave>", hover_out)

    b_exit_score = Button(game_win, text="Exit", height=2, width=26, bg="white", relief="raised",
                          activebackground="#eddbd6", command=lambda: exit_b(game_win), state=NORMAL, font="Forte 16")

    b_exit_score.place(x=400, y=530, anchor="center")
    b_exit_score.bind("<Enter>", hover_in)
    b_exit_score.bind("<Leave>", hover_out)

    # Set up client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8000))

    # Send player name to the server
    client.send(user_name.encode())

# Scoreboard window
def score_board():
    main_win.iconify()

    f = open("scoreBoard.txt", "r")
    score_list = f.read()
    f.close()

    score_window = Toplevel(main_win)
    score_window.title("Score")
    center_window(score_window)
    score_window.geometry("480x640")
    score_window.resizable(0, 0)
    canvas_score = Canvas(score_window, width=480, height=640)
    canvas_score.pack(fill="both", expand=True)
    canvas_score.create_image(0, 0, image=bg_score, anchor="nw")

    canvas_score.create_text(240, 100, text="Score Board", fill="black", font="Forte 30 bold",
                             justify="center")
    canvas_score.create_text(240, 240, text=score_list, fill="black", font="Forte 18", justify="center", anchor="n")
    b_exit_score = Button(score_window, text="Exit", height=2, width=26, bg="white", relief="raised",
                          activebackground="#eddbd6", command=lambda: exit_b(score_window), state=NORMAL, font="Forte 16")

    b_exit_score.place(x=240, y=580, anchor="center")
    b_exit_score.bind("<Enter>", hover_in)
    b_exit_score.bind("<Leave>", hover_out)

# Login window / Enter name
def login():
    main_win.iconify()

    def start_b():
        global user_name
        user_name = enter_name.get()
        print(user_name)
        login_window.destroy()
        new_game()

    login_window = Toplevel(main_win)
    login_window.title("Login")
    login_window.geometry("400x250")
    login_window.resizable(0, 0)
    center_window(login_window)
    canvas_login = Canvas(login_window, width=400, height=250)
    canvas_login.pack(fill="both", expand=True)
    canvas_login.create_image(0, 0, image=bg_login, anchor="nw")

    canvas_login.create_text(200, 40, text="Enter your name", fill="black", font="Forte 26 bold", justify="center")
    enter_name = Entry(canvas_login, width=16, font="Arial 20 bold", justify="center", bg="white")
    canvas_login.create_window(200, 100, window=enter_name)

    b_start = Button(login_window, text="Start", height=1, width=20, bg="white", relief="raised",
                     activebackground="#eddbd6", command=start_b, state=NORMAL, font="Forte 16")
    b_exit_login = Button(login_window, text="Exit", height=1, width=20, bg="white", relief="raised",
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

# Main window
main_win = Tk()
main_win.geometry("640x480")
main_win.resizable(0, 0)
main_win.title("Welcome to the Game!")
center_window(main_win)

user_name = ""
bg_main = PhotoImage(file="images/menu.png")
bg_score = PhotoImage(file="images/score.png")
bg_login = PhotoImage(file="images/login.png")
bg_game = PhotoImage(file="images/game.png")

canvas_main = Canvas(main_win, width=640, height=480)
canvas_main.pack(fill="both", expand=True)
canvas_main.create_image(0, 0, image=bg_main, anchor="nw")

canvas_main.create_text(320, 80, text="Guess the Number", fill="black", font="Forte 30 bold", justify="center",
                        anchor="n")

# Main window buttons
b_new_game = Button(canvas_main, text="New Game", height=2, width=26, bg="white", fg="black", relief="raised",
                    activebackground="#eddbd6", command=login, state=NORMAL, font="Forte 16")
b_score = Button(canvas_main, text="Score", height=2, width=26, bg="white", fg="black", relief="raised",
                 activebackground="#eddbd6", command=score_board, state=NORMAL, font="Forte 16")
b_exit = Button(canvas_main, text="Exit", height=2, width=26, bg="white", fg="black", relief="raised",
                activebackground="#eddbd6", command=main_win.destroy, state=NORMAL, font="Forte 16")

b_new_game.place(x=320, y=220, anchor="center")
b_new_game.bind("<Enter>", hover_in)
b_new_game.bind("<Leave>", hover_out)

b_score.place(x=320, y=290, anchor="center")
b_score.bind("<Enter>", hover_in)
b_score.bind("<Leave>", hover_out)

b_exit.place(x=320, y=360, anchor="center")
b_exit.bind("<Enter>", hover_in)
b_exit.bind("<Leave>", hover_out)

main_win.mainloop()
