import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge and Destroy Aliens")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)  # Power-up color

# Load and resize alien image
alien_image = pygame.image.load("alien.jpg")
alien_image = pygame.transform.scale(alien_image, (50, 50))
alien_width, alien_height = alien_image.get_size()

# Player settings
player_size = 50
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - player_size - 10
player_speed = 7

# Alien settings
alien_speed = 5
alien_spawn_interval = 20  # Higher number means fewer aliens

# Power-up settings
power_up_size = 30
power_up_active = False
power_up_duration = 3000  # Duration in milliseconds (3 seconds)
power_up_start_time = 0
power_up_x = random.randint(0, SCREEN_WIDTH - power_up_size)
power_up_y = random.randint(0, SCREEN_HEIGHT - power_up_size)

# List to keep track of aliens
aliens = []

# Game variables
clock = pygame.time.Clock()
running = True
score = 0
frame_count = 0

# Game loop
while running:
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
        player_x += player_speed

    # Alien spawning
    frame_count += 1
    if frame_count >= alien_spawn_interval:
        frame_count = 0
        alien_x = random.randint(0, SCREEN_WIDTH - alien_width)
        aliens.append([alien_x, -alien_height])  # Start aliens above the screen

    # Move aliens down
    aliens = [[x, y + alien_speed] for x, y in aliens]

    # Remove aliens that have fallen off the screen
    aliens = [alien for alien in aliens if alien[1] < SCREEN_HEIGHT]

    # Power-up spawn check (only if not active)
    if not power_up_active and random.randint(0, 500) < 2:  # Rare spawn chance
        power_up_x = random.randint(0, SCREEN_WIDTH - power_up_size)
        power_up_y = random.randint(0, SCREEN_HEIGHT - power_up_size)

    # Power-up collection
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    power_up_rect = pygame.Rect(power_up_x, power_up_y, power_up_size, power_up_size)
    if player_rect.colliderect(power_up_rect):
        power_up_active = True
        power_up_start_time = pygame.time.get_ticks()  # Activate the power-up

    # Check for power-up timeout
    if power_up_active and pygame.time.get_ticks() - power_up_start_time > power_up_duration:
        power_up_active = False

    # Alien collisions
    for alien in aliens[:]:  # Use a slice to safely remove items
        alien_rect = pygame.Rect(alien[0], alien[1], alien_width, alien_height)
        if player_rect.colliderect(alien_rect):
            if power_up_active:
                aliens.remove(alien)  # Destroy alien if power-up is active
            else:
                print(f"Game Over! Your Score: {score}")
                pygame.quit()
                sys.exit()

    # Update score
    score += 1

    # Fill screen and draw player
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

    # Draw aliens
    for alien in aliens:
        screen.blit(alien_image, (alien[0], alien[1]))

    # Draw power-up (only if not active)
    if not power_up_active:
        pygame.draw.circle(screen, GREEN, (power_up_x + power_up_size // 2, power_up_y + power_up_size // 2), power_up_size // 2)

    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update display and tick clock
    pygame.display.flip()
    clock.tick(30)  # 30 frames per second
