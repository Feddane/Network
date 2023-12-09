import socket
import threading
import pygame
import sys

# Define mole_positions as an empty list
mole_positions = []


# Define mole_radius as a constant
MOLE_RADIUS = 30

# Define a variable to track the player's score
player_score = 0

def pygame_thread():
    global player_names, current_round, score_player1, score_player2, player_score

    # Pygame initialization code
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Whack-a-Mole")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for mole_pos in mole_positions:
                    mole_x, mole_y = mole_pos
                    # Check if the mouse click is inside the mole
                    if (
                        mole_x - MOLE_RADIUS <= mouse_x <= mole_x + MOLE_RADIUS
                        and mole_y - MOLE_RADIUS <= mouse_y <= mole_y + MOLE_RADIUS
                    ):
                        # If the player successfully whacks the mole, increment the score
                        player_score += 1
                        print(f"{user_name} whacked a mole! Score: {player_score}")

        screen.fill((255, 255, 255))

        # Pygame Whack-a-Mole game logic
        for mole_pos in mole_positions:
            pygame.draw.circle(screen, (255, 0, 0), mole_pos, MOLE_RADIUS)

        # Display the player's score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {player_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# Start the Pygame thread
pygame_thread = threading.Thread(target=pygame_thread)
pygame_thread.start()

# Connect to the server
host = '127.0.0.1'
port = 12347


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Get player name from the user
user_name = input("Enter your name: ")
client.send(user_name.encode('utf-8'))

try:
    while True:
        # Receive mole information from the server
        data = client.recv(1024).decode('utf-8')
        if data.startswith("MOLE"):
            _, mole_x, mole_y = data.split()
            mole_x, mole_y = int(mole_x), int(mole_y)

            # Add mole position to the mole_positions list
            mole_positions.append((mole_x, mole_y))

            # Handle mole rendering (not included in this response for brevity)
            # You need to implement the logic to render the mole on the client side

        elif data == "GAME_OVER":
            print("Game over. Final score:", player_score)
            break

        # Handle player's whack (not included in this response for brevity)
        # You need to implement the logic to handle the player's whack

except KeyboardInterrupt:
    print("Game interrupted.")
finally:
    client.close()
