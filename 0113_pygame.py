import pygame
import random
import collections

# --- Configuration ---
WIDTH = 800
HEIGHT = 600
FONT_SIZE = 18
DROP_SPEED = 10  # Lower is faster
COLUMNS = WIDTH // FONT_SIZE

# Matrix colors
BG_COLOR = (0, 0, 0)  # Black
TRAIL_COLOR = (0, 50, 0)  # Dark Green
HEAD_COLOR = (0, 255, 0)  # Bright Green

# Initialize Pygame
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Digital Rain")
clock = pygame.time.Clock()

# Create a font object (None uses the default system font)
font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)

# Use deque to store the y-position of the leading drop for each column
# This creates the persistent "trail" effect
drops = collections.deque([random.randint(0, HEIGHT) for _ in range(COLUMNS)])

# Main loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 2. Draw Background with a slight fade effect
    # Instead of filling the screen completely black, we draw a semi-transparent
    # black surface. This makes old characters fade out slowly.
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BG_COLOR)
    fade_surface.set_alpha(30) # Lower alpha = longer trails
    screen.blit(fade_surface, (0, 0))

    # 3. Update and Draw Drops
    # Remove the last drop position and calculate new positions
    drops.rotate(1)
    
    for i in range(COLUMNS):
        # Get the character (using Matrix-style katakana characters or latin)
        char = chr(random.randint(0x30A0, 0x30FF)) if random.random() > 0.5 else chr(random.randint(33, 126))
        
        # Randomly reset drops to the top to create gaps
        if drops[i] > HEIGHT and random.random() > 0.975:
            drops[i] = random.randint(-50, 0)
        
        # Draw the character
        text = font.render(char, True, HEAD_COLOR)
        text_rect = text.get_rect(center=(i * FONT_SIZE + FONT_SIZE // 2, drops[i]))
        screen.blit(text, text_rect)

    # 4. Update Display
    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()
