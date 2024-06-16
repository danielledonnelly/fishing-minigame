import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishing Game")

# Load images
background_image = pygame.image.load("water.png")
bobber_image = pygame.image.load("bobber.png")
fish_image = pygame.image.load("fish.png")

# Resize images if needed
bobber_image = pygame.transform.scale(bobber_image, (80, 160))  # Bigger dimensions for the bobber
fish_image = pygame.transform.scale(fish_image, (70, 70))  # Bigger dimensions for the fish

# Resize the background to fit the window
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set up clock
clock = pygame.time.Clock()

# Define bobber and fish properties
bobber = pygame.Rect((WIDTH // 2) - 120, (HEIGHT - 160) // 2, 80, 160)
fish = pygame.Rect((WIDTH // 2) - 115, random.randint(0, HEIGHT - 70), 70, 70)

# Bobber movement variables
bobber_speed = 5
bobber_direction = 0

# Fish movement variables
fish_speed = 2
fish_direction = 1  # Initial direction

# Catching mechanics
catch_time = 0
catch_threshold = 5000  # Time in milliseconds required to catch the fish

# Timer
timer_start = 15  # 15 seconds countdown
timer = timer_start
last_time = time.time()

# Game state
game_over = False
game_over_text = ""

# Define the retry button globally
retry_button = pygame.Rect(10, 10, 80, 40)

def draw_window():
    win.blit(background_image, (0, 0))  # Draw the background first

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render(game_over_text, True, (0, 255, 0) if game_over_text == "IT'S A CATCH!" else (255, 0, 0))
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    else:
        # Draw the bobber and fish
        win.blit(bobber_image, (bobber.x, bobber.y))  # Draw bobber next
        win.blit(fish_image, (fish.x, fish.y))  # Draw fish after to ensure it is in front

        # Draw the progress bar container
        container_x = (WIDTH // 2) + 40  # Adjust container to center the game content
        container_y = 50
        container_width = 20
        container_height = HEIGHT - 100
        pygame.draw.rect(win, (200, 200, 200), (container_x - 2, container_y - 2, container_width + 4, container_height + 4))

        # Draw the progress bar
        progress_height = catch_time * container_height / catch_threshold
        pygame.draw.rect(win, (255, 255, 255), (container_x, container_y + container_height - progress_height, container_width, progress_height))

        # Draw the timer
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {int(timer)}", True, (255, 255, 255))
        win.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 20))

    # Draw retry button
    font = pygame.font.Font(None, 36)
    retry_text = font.render("Retry", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), retry_button)
    win.blit(retry_text, (retry_button.x + 5, retry_button.y + 5))

    pygame.display.update()

def move_fish():
    global fish_speed, fish_direction
    # Occasionally change the fish's speed and direction
    if random.randint(0, 100) < 5:  # 5% chance to change direction and speed
        fish_direction = random.choice([-1, 1])
        fish_speed = random.randint(2, 6)  # Random speed between 2 and 6

    fish.y += fish_speed * fish_direction
    fish.y = max(0, min(fish.y, HEIGHT - fish.height))

def reset_game():
    global catch_time, game_over, timer, last_time
    bobber.y = (HEIGHT - 160) // 2
    fish.y = random.randint(0, HEIGHT - 70)
    catch_time = 0
    game_over = False
    timer = timer_start
    last_time = time.time()

run = True
while run:
    current_time = time.time()
    elapsed_time = current_time - last_time
    last_time = current_time

    if not game_over:
        timer -= elapsed_time
        if timer <= 0:
            timer = 0
            game_over = True
            game_over_text = "IT SWAM AWAY..."

    clock.tick(30)  # Frame rate of 30 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_button.collidepoint(event.pos):
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bobber_direction = -1  # Move up
        else:
            bobber_direction = 1   # Move down

        # Move the bobber
        bobber.y += bobber_speed * bobber_direction
        bobber.y = max(0, min(bobber.y, HEIGHT - bobber.height))

        # Move the fish
        move_fish()

        # Check collision and update progress bar
        if bobber.colliderect(fish):
            catch_time += clock.get_time()
            if catch_time >= catch_threshold and bobber.colliderect(fish):
                game_over = True
                game_over_text = "IT'S A CATCH!"
        else:
            catch_time = 0

    # Draw everything
    draw_window()

pygame.quit()
