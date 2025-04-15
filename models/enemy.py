import pygame
from utils.constants import RED, FONT


class Enemy:
    def __init__(self, level):
        self.x, self.y = 600, 300
        self.level = level
        # Scale health and attack power with level
        self.hp = 80 + (level - 1) * 20  # More HP per level
        self.attack_power = 15 + (level - 1) * 8  # More attack per level

        # Load monster image
        self.image = pygame.image.load('images/monster.png')
        # Scale the image based on level (bigger for higher levels)
        size = min(50 + (self.level * 2), 100)  # Cap at size 100
        self.image = pygame.transform.scale(self.image, (size, size))
        # Load health icon
        self.health_icon = pygame.image.load('images/health.png')
        self.health_icon = pygame.transform.scale(self.health_icon, (20, 20))

        # Every 5 levels, give a bigger boost
        if level % 5 == 0:
            self.hp += 50
            self.attack_power += 15

    def draw(self, screen):
        # Draw monster image instead of red rectangle
        screen.blit(self.image, (self.x, self.y))

        # Display level along with HP using health icon
        screen.blit(self.health_icon, (self.x - 50, self.y - 30))
        text = FONT.render(f"Lvl {self.level} Enemy: {max(0, self.hp)}", True,
                           (0, 0, 0))
        screen.blit(text, (self.x - 30, self.y - 30))

    def attack(self):
        # Randomize attack a bit (80-120% of base power)
        import random
        attack_variance = random.uniform(0.8, 1.2)
        return int(self.attack_power * attack_variance)


class Boss(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.hp = int(self.hp * 2)  # Boss has 2× HP
        self.attack_power = int(
            self.attack_power * 1.5)  # Boss has 1.5× attack
        # Make the boss image larger
        size = min(70 + (self.level * 3), 150)  # Cap at size 150
        self.image = pygame.transform.scale(self.image, (size, size))

    def draw(self, screen):
        # Draw boss image
        screen.blit(self.image, (self.x, self.y))

        # Display BOSS label with health icon
        screen.blit(self.health_icon, (self.x - 70, self.y - 30))
        text = FONT.render(f"BOSS Lvl {self.level}: {max(0, self.hp)}",
                           True, (0, 0, 0))
        screen.blit(text, (self.x - 50, self.y - 30))

    def special_attack(self):
        """Boss special attack can deal heavy damage or status effects."""
        import random
        attack_variance = random.uniform(1.5, 2.5)
        return int(self.attack_power * attack_variance)