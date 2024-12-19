import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_SPEED = 10  # Upward movement speed
HORIZONTAL_SPEED = 5  # Horizontal movement speed (left/right)
FALL_SPEED = 1   # Constant downward speed (no increase over time)
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue background color
TEXT_COLOR = (255, 255, 255)  # White text
BORDER_COLOR = (255, 255, 255)  # White border
FONT_SIZE = 32

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("James's Game")

# Load bird image
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))  # Resize image

# Set up font for score and timer
font = pygame.font.Font(None, FONT_SIZE)

# Game variables
bird_x = 100
bird_y = SCREEN_HEIGHT // 3  # Start higher to prevent immediate game over
bird_velocity = 0
bird_horizontal_velocity = 0
game_over = False
score = 0
start_time = time.time()  # Track the time the bird has been in the air
preparing = True  # Flag to handle the 5-second preparation timer

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not game_over:
                bird_velocity = -BIRD_SPEED  # Move bird up when key is pressed
            if event.key == pygame.K_LEFT and not game_over:
                bird_horizontal_velocity = -HORIZONTAL_SPEED  # Move bird left
            if event.key == pygame.K_RIGHT and not game_over:
                bird_horizontal_velocity = HORIZONTAL_SPEED  # Move bird right
            if event.key == pygame.K_r and game_over:
                # Retry the game if 'r' is pressed after game over
                bird_x = 100
                bird_y = SCREEN_HEIGHT // 3
                bird_velocity = 0
                bird_horizontal_velocity = 0
                game_over = False
                score = 0
                start_time = time.time()  # Reset start time
                preparing = True  # Reset preparing state
            if event.key == pygame.K_q and game_over:
                # Quit the game if 'q' is pressed after game over
                pygame.quit()
                quit()

    # Handle preparation timer (5 seconds)
    if preparing:
        preparation_time = int(time.time() - start_time)
        if preparation_time >= 5:  # 5 seconds have passed
            preparing = False
            start_time = time.time()  # Reset the start time for the game timer
        else:
            # Display the preparation countdown
            screen.fill(BACKGROUND_COLOR)
            prep_text = font.render(f"Get Ready! {5 - preparation_time}", True, TEXT_COLOR)
            screen.blit(prep_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.Clock().tick(60)
            continue  # Skip the rest of the loop during preparation

    # Update bird position (after 5 seconds)
    bird_y += bird_velocity
    bird_x += bird_horizontal_velocity

    # Apply constant downward pull (gravity effect)
    bird_velocity += FALL_SPEED  # Constant fall speed, no increasing over time

    # Prevent bird from flying off the top of the screen
    if bird_y < 0:
        bird_y = 0
        bird_velocity = 0

    # Prevent bird from flying off the sides of the screen
    if bird_x < 0:
        bird_x = 0
    if bird_x > SCREEN_WIDTH - BIRD_WIDTH:
        bird_x = SCREEN_WIDTH - BIRD_WIDTH

    # Game over if bird hits the bottom of the screen
    if bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:
        bird_y = SCREEN_HEIGHT - BIRD_HEIGHT
        bird_velocity = 0
        game_over = True

    # Clear screen and redraw background
    screen.fill(BACKGROUND_COLOR)

    # Draw the bird
    screen.blit(bird_image, (bird_x, bird_y))

    # Draw the timer and score
    if not game_over:
        elapsed_time = int(time.time() - start_time)
        score = elapsed_time  # The score is based on how long the bird has been in the air
    score_text = font.render(f"Time: {score} seconds", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    # Draw game over screen
    if game_over:
        game_over_text = font.render("Game Over! Press R to Retry or Q to Quit", True, TEXT_COLOR)
        screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

    # Update the display
    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(60)
