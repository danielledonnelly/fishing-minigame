import pygame
import random

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
bobber_image = pygame.transform.scale(bobber_image, (60, 120))  # New dimensions for the bobber
fish_image = pygame.transform.scale(fish_image, (50, 50))

# Resize the background to fit the window
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set up clock
clock = pygame.time.Clock()

# Define bobber and fish properties
bobber = pygame.Rect((WIDTH - 60) // 2, (HEIGHT - 120) // 2, 60, 120)
fish = pygame.Rect((WIDTH - 50) // 2, random.randint(0, HEIGHT - 50), 50, 50)

# Bobber movement variables
bobber_speed = 5
bobber_direction = 0

# Fish movement variables
fish_speed = 2
fish_direction = 1  # Initial direction

# Catching mechanics
catch_time = 0
catch_threshold = 5000  # Time in milliseconds required to catch the fish

def draw_window():
    win.blit(background_image, (0, 0))  # Draw the background first
    win.blit(bobber_image, (bobber.x, bobber.y))  # Draw bobber next
    win.blit(fish_image, (fish.x, fish.y))  # Draw fish last to ensure it is in front

    if bobber.colliderect(fish):
        global catch_time
        catch_time += clock.get_time()
        pygame.draw.rect(win, (255, 0, 0), (50, 50, catch_time / 10, 20))
        if catch_time >= catch_threshold:
            print("Fish caught!")
            # Reset game or add more logic here
            reset_game()
    else:
        catch_time = 0

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
    global catch_time
    bobber.y = (HEIGHT - 120) // 2
    fish.y = random.randint(0, HEIGHT - 50)
    catch_time = 0

run = True
while run:
    clock.tick(30)  # Frame rate of 30 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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

    # Draw everything
    draw_window()

pygame.quit()