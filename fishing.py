import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display to 1440x810 resolution
WIDTH, HEIGHT = 1440, 810
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Fishing Game")

# Load images
background_image = pygame.image.load("water.png")
bobber_image = pygame.image.load("bobber.png")
fish_image = pygame.image.load("fish.png")
catch_text_image = pygame.image.load("catch-text.png")  # Load catch text overlay
away_text_image = pygame.image.load("away-text.png")    # Load away text overlay

# Resize images if needed
bobber_image = pygame.transform.scale(bobber_image, (80, 160))  # Bigger dimensions for the bobber
fish_image = pygame.transform.scale(fish_image, (70, 70))  # Bigger dimensions for the fish

# Set up clock
clock = pygame.time.Clock()

# Define bobber and fish properties
container_x = (WIDTH // 2) + 40  # Adjust container to center the game content
container_y = 50
container_width = 60  # Adjusted width to 60 pixels
container_height = HEIGHT - 100

bobber = pygame.Rect((WIDTH // 2) - 120, (container_y + container_height // 2) - 80, 80, 160)
fish = pygame.Rect((WIDTH // 2) - 115, random.randint(container_y, container_y + container_height - 70), 70, 70)

# Bobber movement variables
bobber_speed = 5
bobber_direction = 0

# Fish movement variables
fish_speed = 2
fish_direction = 1  # Initial direction

# Catching mechanics
catch_time = 0
catch_threshold = 5000  # Time in milliseconds required to catch the fish
catch_decrement = 50  # Decrement speed for the catch time when the bobber loses the fish

# Timer
timer_start = 10  # 15 seconds countdown
timer = timer_start
last_time = time.time()

# Game state
game_over = False
game_over_text = ""

# Define the retry button globally
retry_button = pygame.Rect(10, 10, 80, 40)

def draw_window():
    # Fill background with black
    win.fill((0, 0, 0))

    # Get current window size
    current_width, current_height = win.get_size()

    # Resize the background image to fit the current window size
    scaled_background = pygame.transform.scale(background_image, (current_width, current_height))
    win.blit(scaled_background, (0, 0))

    # Calculate the position to center the game content
    content_x = (current_width - WIDTH) // 2
    content_y = (current_height - HEIGHT) // 2

    if game_over:
        if game_over_text == "IT'S A CATCH!":
            win.blit(catch_text_image, (content_x, content_y))
        else:
            win.blit(away_text_image, (content_x, content_y))
    else:
        # Draw the bobber and fish centered
        win.blit(bobber_image, (bobber.x + content_x, bobber.y + content_y))
        win.blit(fish_image, (fish.x + content_x, fish.y + content_y))

        # Draw the progress bar container centered
        pygame.draw.rect(win, (200, 200, 200), (container_x - 2 + content_x, container_y - 2 + content_y, container_width + 4, container_height + 4))

        # Draw the progress bar centered
        progress_height = catch_time * container_height / catch_threshold
        pygame.draw.rect(win, (255, 255, 255), (container_x + content_x, container_y + container_height - progress_height + content_y, container_width, progress_height))

        # Draw the timer rectangle and text
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {int(timer)}", True, (255, 255, 255))
        timer_rect = pygame.Rect(content_x + WIDTH - timer_text.get_width() - 30, content_y + 10, timer_text.get_width() + 20, timer_text.get_height() + 10)
        pygame.draw.rect(win, (22, 76, 114), timer_rect)  # Rectangle color #164C72
        win.blit(timer_text, (timer_rect.x + 10, timer_rect.y + 5))

    # Draw retry button rectangle and text
    font = pygame.font.Font(None, 36)
    retry_text = font.render("Retry", True, (255, 255, 255))  # White text
    retry_rect = pygame.Rect(retry_button.x + content_x, retry_button.y + content_y, retry_text.get_width() + 20, retry_text.get_height() + 10)
    pygame.draw.rect(win, (22, 76, 114), retry_rect)  # Rectangle color #164C72
    win.blit(retry_text, (retry_rect.x + 10, retry_rect.y + 5))

    pygame.display.update()

def move_fish():
    global fish_speed, fish_direction
    # Occasionally change the fish's speed and direction
    if random.randint(0, 100) < 5:  # 5% chance to change direction and speed
        fish_direction = random.choice([-1, 1])
        fish_speed = random.randint(2, 6)  # Random speed between 2 and 6

    fish.y += fish_speed * fish_direction
    fish.y = max(container_y, min(fish.y, container_y + container_height - fish.height))

def reset_game():
    global catch_time, game_over, timer, last_time, game_over_text
    bobber.y = (container_y + container_height // 2) - 80
    fish.y = random.randint(container_y, container_y + container_height - 70)
    catch_time = 0
    game_over = False
    timer = timer_start
    last_time = time.time()
    game_over_text = ""

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
            # Adjust the click position to account for the centered content
            click_x, click_y = event.pos
            click_x -= (win.get_width() - WIDTH) // 2
            click_y -= (win.get_height() - HEIGHT) // 2
            if retry_button.collidepoint((click_x, click_y)):
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bobber_direction = -1  # Move up
        else:
            bobber_direction = 1   # Move down

        # Move the bobber
        bobber.y += bobber_speed * bobber_direction
        bobber.y = max(container_y, min(bobber.y, container_y + container_height - bobber.height + 2))

        # Move the fish
        move_fish()

        # Check collision and update progress bar
        if bobber.colliderect(fish):
            catch_time += clock.get_time()
            if catch_time >= catch_threshold and not game_over:
                game_over = True
                game_over_text = "IT'S A CATCH!"
        else:
            catch_time -= catch_decrement
            catch_time = max(0, catch_time)  # Ensure catch_time doesn't go below 0

    # Draw everything
    draw_window()

    # Additional check to ensure game state consistency
    if game_over and game_over_text != "IT'S A CATCH!":
        if catch_time < catch_threshold:
            game_over_text = "IT SWAM AWAY..."

pygame.quit()