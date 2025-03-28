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
        
        
 