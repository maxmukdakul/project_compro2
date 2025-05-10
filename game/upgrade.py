import pygame
from utils.display import display_text
from utils.constants import WHITE
import data_collector


def upgrade_menu(hero, screen, background):
    choosing = True
    while choosing:
        screen.blit(background, (0, 0))  # Use background image
        display_text(screen, "Choose an upgrade:", 300, 200)
        display_text(screen, "1. Strength +1", 300, 240)
        display_text(screen, "2. Magic +1", 300, 280)
        display_text(screen, "3. Speed +0.1", 300, 320)
        display_text(screen, "4. Health +50", 300, 360)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    hero.strength_level += 1
                    # Track the strength upgrade
                    data_collector.track_upgrade(hero.current_level,
                                                 "Strength",
                                                 hero.strength_level)
                    choosing = False
                elif event.key == pygame.K_2:
                    hero.magic_level += 1
                    # Track the magic upgrade
                    data_collector.track_upgrade(hero.current_level, "Magic",
                                                 hero.magic_level)
                    choosing = False
                elif event.key == pygame.K_3:
                    hero.speed += 0.1
                    # Track the speed upgrade
                    data_collector.track_upgrade(hero.current_level, "Speed",
                                                 hero.speed)
                    choosing = False
                elif event.key == pygame.K_4:
                    hero.max_hp += 50
                    hero.hp += 50
                    # Track the health upgrade
                    data_collector.track_upgrade(hero.current_level, "Health",
                                                 hero.max_hp)
                    choosing = False

                # Give coins after any upgrade
                if not choosing:
                    hero.coins += 10