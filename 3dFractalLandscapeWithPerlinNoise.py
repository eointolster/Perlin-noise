import pygame
import numpy as np
from noise import pnoise2

# Constants
WIDTH = 800
HEIGHT = 600
SCALE = 20
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0
SPEED = 0.1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Generate fractal landscape
def generate_landscape(offset_x, offset_y):
    landscape = np.zeros((WIDTH // SCALE, HEIGHT // SCALE))
    for y in range(HEIGHT // SCALE):
        for x in range(WIDTH // SCALE):
            nx = (x + offset_x) / (WIDTH // SCALE) - 0.5
            ny = (y + offset_y) / (HEIGHT // SCALE) - 0.5
            value = pnoise2(nx, ny, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY)
            landscape[x][y] = value
    return landscape

# Color mapping function
def map_color(value):
    r = int(np.clip((value + 1) * 128, 0, 255))
    g = int(np.clip((value + 0.5) * 128, 0, 255))
    b = int(np.clip(value * 128, 0, 255))
    return (r, g, b)

# Main game loop
offset_x = 0
offset_y = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update offset based on arrow key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        offset_x -= SPEED
    if keys[pygame.K_RIGHT]:
        offset_x += SPEED
    if keys[pygame.K_UP]:
        offset_y -= SPEED
    if keys[pygame.K_DOWN]:
        offset_y += SPEED

    # Generate and render fractal landscape
    landscape = generate_landscape(offset_x, offset_y)
    for y in range(HEIGHT // SCALE):
        for x in range(WIDTH // SCALE):
            value = landscape[x][y]
            color = map_color(value)
            pygame.draw.rect(screen, color, (x * SCALE, y * SCALE, SCALE, SCALE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()