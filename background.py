import pygame
from utils.constants import WIDTH, HEIGHT


def create_game_background(wall_image_path='images/bigwall.png'):
    """Create a background using the wall image plus a platform"""
    # Load and scale the wall image
    wall_image = pygame.image.load(wall_image_path)
    wall_image = pygame.transform.scale(wall_image, (WIDTH, HEIGHT))

    # Create background surface
    background = pygame.Surface((WIDTH, HEIGHT))
    background.blit(wall_image, (0, 0))

    # Create the brown land platform
    land_height = 150
    land_y = HEIGHT - land_height
    land = pygame.Rect(0, land_y, WIDTH, land_height)
    pygame.draw.rect(background, (139, 69, 19), land)  # Brown color for land

    # Add some texture to the land
    for y in range(land_y, HEIGHT, 10):
        for x in range(0, WIDTH, 30):
            offset = 15 if (y // 10) % 2 == 0 else 0
            pygame.draw.line(background, (120, 60, 10),
                             (x + offset, y), (x + offset + 10, y), 1)

    return background