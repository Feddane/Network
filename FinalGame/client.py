import socket
import threading
import pygame
import sys

# Client Constants
HOST = '127.0.0.1'
PORT = 5555

# Game Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
MOLE_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Client variables
client_id = 0

def receive_mole_coordinates(client_socket):
    global client_id

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            x, y, client_id = map(int, data.split(','))
            return x, y

        except Exception as e:
            print(f"Error receiving mole coordinates: {e}")
            break

def send_whack_event(client_socket):
    try:
        client_socket.send("whack".encode('utf-8'))
    except Exception as e:
        print(f"Error sending whack event: {e}")

def draw_mole(screen, x, y):
    pygame.draw.circle(screen, RED, (x, y), MOLE_SIZE)

def show_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over(screen, final_score):
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    final_score_text = font.render(f"Final Score: {final_score}", True, RED)
    screen.blit(final_score_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))

    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def main():
    global client_id

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Whack-a-Mole Client")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                send_whack_event(client_socket)

        x, y = receive_mole_coordinates(client_socket)
        draw_mole(screen, x, y)
        show_score(screen, client_id)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
