import pygame

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800  # Set your desired screen width
SCREEN_HEIGHT = 600  # Set your desired screen height

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the image
bg_image = pygame.image.load("assets/images/backgrounds/Cartoon_Forest_BG_01.png")

# Scale the image to fit the screen (optional, only if needed)
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Calculate position to center the image
bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background image centered
    screen.blit(bg_image, bg_rect.topleft)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()