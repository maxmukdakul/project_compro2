import pygame
import random
from utils.constants import BLUE, FONT

class Hero:
    def __init__(self):
        self.x, self.y = 100, 300
        self.hp = 100
        self.max_hp = 100
        self.magic_level = 3
        self.strength_level = 3
        self.speed = 0.1
        self.coins = 0
        # Load character image
        self.image = pygame.image.load('images/character.png')
        # Scale the image if needed (adjust size as appropriate)
        self.image = pygame.transform.scale(self.image, (50, 50))
        # Load health icon
        self.health_icon = pygame.image.load('images/health.png')
        self.health_icon = pygame.transform.scale(self.health_icon, (20, 20))

    def draw(self, screen):
        # Draw character image instead of blue rectangle
        screen.blit(self.image, (self.x, self.y))
        # Draw health icon instead of "HP" text
        screen.blit(self.health_icon, (self.x - 20, self.y - 30))
        text = FONT.render(f": {max(0, self.hp)}/{self.max_hp}", True, (0, 0, 0))
        screen.blit(text, (self.x, self.y - 30))

    # Rest of the methods remain unchanged
    def attack_magic(self):
        return self.magic_level * 10

    def attack_strength(self):
        return self.strength_level * 10

    def get_magic_power(self):
        return self.magic_level * 10

    def get_attack_power(self):
        return self.strength_level * 10

    def defend(self, enemy_damage):
        return max(0, enemy_damage - (self.strength_level * 2))

    def heal(self):
        previous_hp = self.hp  # Store HP before healing
        self.hp = min(self.max_hp, self.hp + self.magic_level * 10)
        return self.hp - previous_hp  # Return actual healed amount

    def dodge(self):
        return random.random() < self.speed