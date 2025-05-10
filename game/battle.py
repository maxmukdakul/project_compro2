import pygame
from utils.display import display_text
from utils.constants import WHITE, GREEN, HEIGHT, WIDTH
import data_collector


class Battle:
    def __init__(self, hero, enemy, level, screen, game, background):
        self.hero = hero
        self.enemy = enemy
        self.level = level
        self.screen = screen
        self.game = game
        self.background = background
        self.battle_running = True
        self.hero_action_taken = False

        # Position characters on the platform
        land_height = 150
        self.land_y = HEIGHT - land_height
        self.hero.y = self.land_y - 50
        self.enemy.y = self.land_y - 50

        # Create clickable skill buttons in a 2x2 grid with grey color
        # Make buttons smaller
        button_width, button_height = 150, 50
        button_spacing_h = 20
        button_spacing_v = 10

        # Calculate positions for 2x2 grid within brown area
        # Position them at the bottom of the screen with padding
        bottom_padding = 20
        left_column_x = WIDTH // 4 - button_width // 2
        right_column_x = 3 * WIDTH // 4 - button_width // 2

        # Calculate vertical positions to ensure buttons are in brown area
        # and don't cover hero/enemy
        bottom_row_y = HEIGHT - bottom_padding - button_height
        top_row_y = bottom_row_y - button_height - button_spacing_v

        # Grey color for all buttons
        button_color = (128, 128, 128)  # Grey

        self.skill_buttons = [
            {
                "rect": pygame.Rect(left_column_x, top_row_y, button_width,
                                    button_height),
                "text": "Magic Attack",
                "action": self.use_magic_attack,
                "color": button_color
            },
            {
                "rect": pygame.Rect(right_column_x, top_row_y, button_width,
                                    button_height),
                "text": "Strength Attack",
                "action": self.use_strength_attack,
                "color": button_color
            },
            {
                "rect": pygame.Rect(left_column_x, bottom_row_y, button_width,
                                    button_height),
                "text": "Defend",
                "action": self.use_defend,
                "color": button_color
            },
            {
                "rect": pygame.Rect(right_column_x, bottom_row_y, button_width,
                                    button_height),
                "text": "Heal",
                "action": self.use_heal,
                "color": button_color
            }
        ]

        # Animation effect variables
        self.animation_text = None
        self.animation_pos = None
        self.animation_color = None
        self.animation_timer = 0

    def use_magic_attack(self):
        damage = self.hero.attack_magic()
        self.enemy.hp -= damage
        self.show_animation(f"-{damage}", self.enemy.x, self.enemy.y - 30,
                            (100, 100, 255))
        self.hero_action_taken = True
        # Track the skill usage and damage dealt
        data_collector.track_skill_use(self.level, "Magic Attack", damage)
        data_collector.track_damage(self.level, damage, "Magic")

    def use_strength_attack(self):
        damage = self.hero.attack_strength()
        self.enemy.hp -= damage
        self.show_animation(f"-{damage}", self.enemy.x, self.enemy.y - 30,
                            (255, 100, 100))
        self.hero_action_taken = True
        # Track the skill usage and damage dealt
        data_collector.track_skill_use(self.level, "Strength Attack", damage)
        data_collector.track_damage(self.level, damage, "Strength")

    def use_defend(self):
        enemy_damage = self.enemy.attack()
        reduced_damage = self.hero.defend(enemy_damage)
        self.hero.hp -= reduced_damage
        self.show_animation("Defended!", self.hero.x, self.hero.y - 30,
                            (100, 255, 100))
        self.hero_action_taken = True
        # Track the skill usage
        data_collector.track_skill_use(self.level, "Defend", reduced_damage)

    def use_heal(self):
        healed_amount = self.hero.heal()
        self.show_animation(f"+{healed_amount} HP", self.hero.x,
                            self.hero.y - 30, (255, 255, 100))
        self.hero_action_taken = True
        # Track the skill usage
        data_collector.track_skill_use(self.level, "Heal", healed_amount)

        # Enemy attack after healing (only if hero didn't dodge)
        if not self.hero.dodge():
            damage = self.enemy.attack()
            self.hero.hp -= damage
            # Show damage after a short delay
            pygame.time.delay(300)
            self.show_animation(f"-{damage}", self.hero.x, self.hero.y - 60,
                                (255, 0, 0))

    def show_animation(self, text, x, y, color):
        """Store animation data to display for a few frames"""
        self.animation_text = text
        self.animation_pos = (x, y)
        self.animation_color = color
        self.animation_timer = 30  # Display for 30 frames

    def run(self):
        while self.battle_running:
            # Use background image
            self.screen.blit(self.background, (0, 0))

            # Draw characters first so they appear above UI elements
            self.hero.draw(self.screen)
            self.enemy.draw(self.screen)

            # Then draw UI including buttons
            self.display_battle_ui()

            # Handle animations
            if self.animation_timer > 0:
                display_text(self.screen, self.animation_text,
                             self.animation_pos[0], self.animation_pos[1],
                             self.animation_color, 40, True)
                self.animation_timer -= 1

            pygame.display.flip()

            self.hero_action_taken = False
            self.handle_events()

            if not self.hero_action_taken:
                continue

            # Process combat results after action is taken
            if self.process_combat():
                return True  # Battle won

        return False  # Battle lost or quit

    def display_battle_ui(self):
        """Display battle UI elements with clickable skill blocks"""
        # Display floor level
        display_text(self.screen, f"Floor {self.level}", 20, 20)

        # Display health info at top of screen
        self.screen.blit(self.hero.health_icon, (30, 50))
        display_text(self.screen, f": {self.hero.hp}/{self.hero.max_hp}", 50,
                     50)

        # Enemy health
        self.screen.blit(self.enemy.health_icon, (WIDTH - 250, 50))
        display_text(self.screen,
                     f"Lvl {self.level} Enemy: {max(0, self.enemy.hp)}",
                     WIDTH - 230, 50)

        # Draw skill buttons
        for button in self.skill_buttons:
            # Draw button background
            pygame.draw.rect(self.screen, button["color"], button["rect"])
            # Draw button border
            pygame.draw.rect(self.screen, (0, 0, 0), button["rect"], 2)
            # Center text on button
            text_x = button["rect"].x + button["rect"].width // 2
            text_y = button["rect"].y + button["rect"].height // 2
            display_text(self.screen, button["text"], text_x, text_y,
                         (255, 255, 255), 24,
                         True)  # Smaller white text for better fit

    def handle_events(self):
        """Process user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if any skill button was clicked
                mouse_pos = pygame.mouse.get_pos()
                for button in self.skill_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["action"]()  # Call the associated action
                        break

    def process_combat(self):
        """Process the combat results and determine if battle continues"""
        # After player action, enemy counterattacks (except after healing which has its own logic)
        if self.hero_action_taken and self.enemy.hp > 0 and self.hero.hp > 0:
            # Only counterattack if we didn't just heal (heal has its own enemy attack logic)
            if not any(
                    button["text"] == "Heal" and button["rect"].collidepoint(
                        pygame.mouse.get_pos())
                    for button in self.skill_buttons):
                if not self.hero.dodge():
                    damage = self.enemy.attack()
                    self.hero.hp -= damage
                    # Show enemy attack after a short delay
                    pygame.time.delay(300)
                    self.show_animation(f"-{damage}", self.hero.x,
                                        self.hero.y - 30, (255, 0, 0))
                    pygame.display.flip()
                    pygame.time.delay(300)  # Pause to see the damage

        # Check win/loss conditions
        if self.hero.hp <= 0:
            # Record health data before game over
            data_collector.track_health(self.level, 0, self.hero.max_hp)
            self.game.game_over()
            pygame.time.delay(1000)
            self.battle_running = False
            return False

        if self.enemy.hp <= 0:
            # Record health data after winning
            data_collector.track_health(self.level, self.hero.hp, self.hero.max_hp)
            self.battle_running = False
            return True

        return None  # Battle continues


def battle(hero, enemy, level, screen, game, background):
    """Legacy function for backward compatibility"""
    # Store current level in hero for tracking purposes
    hero.current_level = level
    battle_instance = Battle(hero, enemy, level, screen, game, background)
    return battle_instance.run()