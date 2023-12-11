import socket
import pickle
import pygame

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# Pygame setup
pygame.init()

# Initialize the Pygame screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Whack-a-Mole Client")

# Function to draw moles
def draw_moles(moles):
    for mole in moles:
        if mole['active']:
            pygame.draw.rect(screen, (255, 0, 0), mole['rect'])

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the player clicked on an active mole
            click_position = pygame.mouse.get_pos()
            for mole in moles:
                if mole['rect'].collidepoint(click_position) and mole['active']:
                    mole['active'] = False
                    # Send a whack event to the server (for scoring)
                    client_socket.send(b'whack')

    # Receive moles from the server
    moles = pickle.loads(client_socket.recv(1024))

    # Update the screen
    screen.fill((0, 0, 0))
    draw_moles(moles)

    pygame.display.flip()
    clock.tick(60)
