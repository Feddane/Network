import socket
import threading
import pickle
import pygame

# Client configuration
SERVER = '127.0.0.1'
PORT = 5555

# Initialize Pygame
pygame.init()

# Pygame window settings
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
WHITE = (255, 255, 255)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

# Ball dimensions
BALL_SIZE = 20

# Client class to handle networking
class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER, PORT))
        self.paddle1_pos = [50, 250]
        self.paddle2_pos = [750, 250]
        self.ball_pos = [400, 300]

    def send_position(self):
        pos_data = {"paddle1_pos": self.paddle1_pos, "paddle2_pos": self.paddle2_pos}
        self.client_socket.send(pickle.dumps(pos_data))

    def receive_data(self):
        while True:
            try:
                data = pickle.loads(self.client_socket.recv(1024))
                # Update game state based on received data
                self.ball_pos = data["ball_pos"]
                self.paddle1_pos = data["paddle1_pos"]
                self.paddle2_pos = data["paddle2_pos"]
            except:
                break

# Game loop
def game_loop(client):
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        # Update player position based on key presses
        if keys[pygame.K_w] and client.paddle1_pos[1] > 0:
            client.paddle1_pos[1] -= 5
        if keys[pygame.K_s] and client.paddle1_pos[1] < HEIGHT - PADDLE_HEIGHT:
            client.paddle1_pos[1] += 5

        # Update player position based on key presses for paddle 2
        if keys[pygame.K_UP] and client.paddle2_pos[1] > 0:
            client.paddle2_pos[1] -= 5
        if keys[pygame.K_DOWN] and client.paddle2_pos[1] < HEIGHT - PADDLE_HEIGHT:
            client.paddle2_pos[1] += 5

        # Send player position to the server
        client.send_position()

        # Draw paddles and ball on the screen
        win.fill(WHITE)
        pygame.draw.rect(win, (0, 128, 255), (client.paddle1_pos[0], client.paddle1_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(win, (255, 0, 0), (client.paddle2_pos[0], client.paddle2_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(win, (255, 255, 0), (client.ball_pos[0], client.ball_pos[1], BALL_SIZE, BALL_SIZE))
        pygame.display.update()

        clock.tick(60)

# Run the client
if __name__ == "__main__":
    client = Client()

    # Start a thread to handle data reception from the server
    receive_thread = threading.Thread(target=client.receive_data)
    receive_thread.start()

    # Run the game loop
    game_loop(client)
