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

# Load background image
background_image = pygame.image.load("space.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)  # Power-up color

# Load and resize power-up image
power_up_image = pygame.image.load("power up.jpg")
power_up_image = pygame.transform.scale(power_up_image, (40, 40))
power_up_width, power_up_height = power_up_image.get_size()  # Get size after resizing

# Load and resize player image
player_image = pygame.image.load("troll.jpg")
player_image = pygame.transform.scale(player_image, (50, 50))
player_width, player_height = player_image.get_size()
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 7
player_health = 3  # Health system: can take 3 hits before game over

# Bullet settings
bullet_width, bullet_height = 10, 20
bullet_speed = 10
bullets = []  # List to store active bullets

# Alien settings
alien_spawn_interval = 5  # Lower interval for more frequent spawns

# Expanded alien size and speed spectrum
ALIEN_MIN_SIZE = 20
ALIEN_MAX_SIZE = 120
ALIEN_MIN_SPEED = 2
ALIEN_MAX_SPEED = 10

# Power-up settings
power_up_active = False
power_up_duration = 5000  # Duration in milliseconds (5 seconds)
power_up_start_time = 0
power_up_visible = False
power_up_x, power_up_y = 0, player_y  # Fixed spawn height to player level

# List to keep track of aliens with their properties
aliens = []

# Game variables
clock = pygame.time.Clock()
running = True
game_started = False  # To track if the game has started
score = 0
frame_count = 0

def show_start_screen():
    """Display the starting screen."""
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 48)
    start_text = font.render("Hi! Welcome to literally the best game, now die!!!!!!!!!!!", True, (255, 0, 0))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    
    # Wait for any key press to start
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_end_screen(score):
    """Display end screen with final score after game over."""
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 48)
    end_text = font.render("You died, stinky hahaha", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (0, 0, 0))
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()
    
    pygame.time.delay(5000)  # Show end screen for 5 seconds
    pygame.quit()
    sys.exit()

# Show start screen before game begins
show_start_screen()
game_started = True

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
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE] and power_up_active:
        # Shoot bullet if power-up is active
        bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

    # Alien spawning
    frame_count += 1
    if frame_count >= alien_spawn_interval:
        frame_count = 0
        # Generate a random size and speed for the alien
        alien_size = random.randint(ALIEN_MIN_SIZE, ALIEN_MAX_SIZE)
        alien_speed = ALIEN_MAX_SPEED - ((alien_size - ALIEN_MIN_SIZE) / (ALIEN_MAX_SIZE - ALIEN_MIN_SIZE)) * (ALIEN_MAX_SPEED - ALIEN_MIN_SPEED)
        alien_image = pygame.transform.scale(pygame.image.load("alien.jpg"), (alien_size, alien_size))

        # Spawn the alien at a random horizontal position at the top
        alien_x = random.randint(0, SCREEN_WIDTH - alien_size)
        aliens.append({'image': alien_image, 'x': alien_x, 'y': -alien_size, 'speed': alien_speed, 'size': alien_size})

    # Move aliens down
    for alien in aliens:
        alien['y'] += alien['speed']

    # Remove aliens that have fallen off the screen
    aliens = [alien for alien in aliens if alien['y'] < SCREEN_HEIGHT]

    # Power-up spawn logic
    if not power_up_visible and random.randint(0, 100) < 2:  # Adjust spawn frequency as needed
        power_up_x = random.randint(max(0, player_x - 100), min(SCREEN_WIDTH - power_up_width, player_x + 100))
        power_up_y = player_y  # Spawn at player level
        power_up_visible = True

    # Power-up collection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    power_up_rect = pygame.Rect(power_up_x, power_up_y, power_up_width, power_up_height)
    if power_up_visible and player_rect.colliderect(power_up_rect):
        power_up_active = True
        power_up_start_time = pygame.time.get_ticks()
        power_up_visible = False  # Hide power-up after collection

    # Check for power-up timeout
    if power_up_active and pygame.time.get_ticks() - power_up_start_time > power_up_duration:
        power_up_active = False

    # Move bullets
    bullets = [[x, y - bullet_speed] for x, y in bullets if y > 0]

    # Check bullet collisions with aliens
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for alien in aliens[:]:
            alien_rect = pygame.Rect(alien['x'], alien['y'], alien['size'], alien['size'])
            if bullet_rect.colliderect(alien_rect):
                aliens.remove(alien)
                bullets.remove(bullet)
                score += 100  # Increase score for killing an alien
                break

    # Alien collisions
    for alien in aliens[:]:  # Use a slice to safely remove items
        alien_rect = pygame.Rect(alien['x'], alien['y'], alien['size'], alien['size'])
        if player_rect.colliderect(alien_rect):
            aliens.remove(alien)
            player_health -= 1  # Reduce health on collision
            if player_health <= 0:
                show_end_screen(score)  # Show end screen with score if health reaches 0

    # Update score
    score += 1

    # Fill screen and draw background
    screen.blit(background_image, (0, 0))
    
    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw aliens
    for alien in aliens:
        screen.blit(alien['image'], (alien['x'], alien['y']))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw power-up (only if not active and visible)
    if not power_up_active and power_up_visible:
        screen.blit(power_up_image, (power_up_x, power_up_y))

    # Draw score and health
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    health_text = font.render(f"Health: {player_health}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    # Update display and tick clock
    pygame.display.flip()
    clock.tick(30)  # 30 frames per second
