import pygame
import numpy as np
from noise import pnoise2

# Constants
WIDTH = 800
HEIGHT = 600
SCALE = 10
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0
SPEED = 1.0
ZOOM_SPEED = 0.1
MINIMAP_SIZE = 100

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Generate fractal landscape
def generate_landscape(offset_x, offset_y, zoom):
    landscape = np.zeros((WIDTH // SCALE, HEIGHT // SCALE))
    for y in range(HEIGHT // SCALE):
        for x in range(WIDTH // SCALE):
            nx = (x + offset_x) * zoom / (WIDTH // SCALE) - 0.5
            ny = (y + offset_y) * zoom / (HEIGHT // SCALE) - 0.5
            value = pnoise2(nx, ny, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY)
            landscape[x][y] = value
    return landscape

# Color mapping function
def map_color(value):
    if value < -0.2:
        # Deep blue for oceans and lakes
        return (0, 0, 128)
    elif value < 0.2:
        # Green for middle height
        return (0, 255, 0)
    elif value < 0.4:
        # Gray for high elevation
        return (128, 128, 128)
    else:
        # White for snow-capped peaks
        return (255, 255, 255)

# Main game loop
offset_x = 0
offset_y = 0
zoom = 1.0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update offset and zoom based on key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        offset_x -= SPEED * zoom
    if keys[pygame.K_RIGHT]:
        offset_x += SPEED * zoom
    if keys[pygame.K_UP]:
        offset_y -= SPEED * zoom
    if keys[pygame.K_DOWN]:
        offset_y += SPEED * zoom
    if keys[pygame.K_w]:
        zoom *= (1 + ZOOM_SPEED)
    if keys[pygame.K_s]:
        zoom *= (1 - ZOOM_SPEED)

    # Generate and render fractal landscape
    landscape = generate_landscape(offset_x, offset_y, zoom)
    for y in range(HEIGHT // SCALE):
        for x in range(WIDTH // SCALE):
            value = landscape[x][y]
            color = map_color(value)
            pygame.draw.rect(screen, color, (x * SCALE, y * SCALE, SCALE, SCALE))

    # Render minimap
    minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
    minimap_surface.fill((200, 200, 200))
    minimap_landscape = generate_landscape(offset_x, offset_y, 0.1)
    for y in range(MINIMAP_SIZE):
        for x in range(MINIMAP_SIZE):
            value = minimap_landscape[x * (WIDTH // SCALE) // MINIMAP_SIZE][y * (HEIGHT // SCALE) // MINIMAP_SIZE]
            color = map_color(value)
            minimap_surface.set_at((x, y), color)
    screen.blit(minimap_surface, (WIDTH - MINIMAP_SIZE - 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()