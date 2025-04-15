import pygame
from utils.constants import BLACK

def display_text(screen, text, x, y, color=BLACK, font_size=36, center=False):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
