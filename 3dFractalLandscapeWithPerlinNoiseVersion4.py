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
SPEED = 1.0
ZOOM_SPEED = 0.1
ANGLE = 45

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
        # Green for grass blocks
        return (0, 255, 0)
    elif value < 0.4:
        # Brown for dirt blocks
        return (139, 69, 19)
    else:
        # Gray for stone blocks
        return (128, 128, 128)

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

    # Generate fractal landscape
    landscape = generate_landscape(offset_x, offset_y, zoom)

    # Clear the screen
    screen.fill((135, 206, 235))  # Sky blue color

    # Render fractal landscape in 3D
    for y in range(HEIGHT // SCALE - 1, -1, -1):
        for x in range(WIDTH // SCALE):
            value = landscape[x][y]
            color = map_color(value)
            height = int(value * SCALE)
            points = [
                (x * SCALE, y * SCALE),
                ((x + 1) * SCALE, y * SCALE),
                ((x + 1) * SCALE, (y + 1) * SCALE),
                (x * SCALE, (y + 1) * SCALE)
            ]
            # Adjust points for 3D effect
            points = [(p[0] - height, p[1] - height) for p in points]
            pygame.draw.polygon(screen, color, points)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()