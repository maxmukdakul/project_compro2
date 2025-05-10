import pygame
from models.player import Hero
from models.enemy import Enemy
from game.shop import Shop
from game.battle import battle
from game.upgrade import upgrade_menu
from utils.constants import WIDTH, HEIGHT, WHITE
from utils.display import display_text
from background import create_game_background
import data_collector


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.initialize_game()

        # Load additional images
        self.coin_image = pygame.image.load('images/coins.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (20, 20))

    def initialize_game(self):
        """Initialize or reset all game states and objects"""
        self.hero = Hero()  # Initialize the player (hero)
        self.enemy = Enemy(level=1)  # Initialize an enemy for the demo
        self.shop_open = False  # Track if the shop is open
        self.show_characters = True  # Add this flag
        self.shop_button = pygame.Rect(WIDTH - 150, 20, 120,
                                       40)  # Shop button in top right
        self.current_level = 1  # Track the current level
        self.enemies_defeated = 0  # Track how many enemies have been defeated

        # Set the hero's current level attribute for data collection
        self.hero.current_level = self.current_level

        # Create the background with platform
        self.background = create_game_background()

        # Position characters on the platform
        land_height = 150
        land_y = HEIGHT - land_height
        self.hero.y = land_y - 50  # 50 is the height of the character
        self.enemy.y = land_y - 50  # Position enemy on platform too
        self.game_running = True

    def run(self):
        self.game_running = True
        while self.game_running:
            self.screen.blit(self.background, (0, 0))
            self.handle_events()

            if not self.shop_open:
                if self.show_characters:
                    self.hero.draw(self.screen)
                    self.enemy.draw(self.screen)
                self.display_hero_stats()
                pygame.draw.rect(self.screen, (200, 200, 200),
                                 self.shop_button)
                display_text(self.screen, "Shop", WIDTH - 105, 30)
                display_text(self.screen, f"Level: {self.current_level}",
                             WIDTH // 2 - 50, 20)
                display_text(self.screen, "Click on the enemy to battle",
                             WIDTH // 2 - 150, HEIGHT // 2)

            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        """Handle all user events, including input and quitting."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if shop button was clicked
                if self.shop_button.collidepoint(mouse_x, mouse_y):
                    self.shop_open = True
                    self.open_shop()

                # Check if enemy was clicked
                enemy_rect = pygame.Rect(self.enemy.x, self.enemy.y, 50, 50)
                if enemy_rect.collidepoint(mouse_x, mouse_y):
                    self.start_battle()

            # Keep the debug key
            elif event.type == pygame.KEYDOWN:
                # Debug key - print positions
                if event.key == pygame.K_d:
                    print(f"Hero: ({self.hero.x}, {self.hero.y})")
                    print(f"Enemy: ({self.enemy.x}, {self.enemy.y})")
                    print(f"Current level: {self.current_level}")
                    print(
                        f"Enemy stats - HP: {self.enemy.hp}, ATK: {self.enemy.attack_power}")

    def display_hero_stats(self):
        """Display hero stats (HP and Coins)."""
        # Draw health icon
        self.screen.blit(self.hero.health_icon, (30, 50))
        display_text(self.screen, f": {self.hero.hp}/{self.hero.max_hp}", 50,
                     50)
        # Draw coin image before coin text
        self.screen.blit(self.coin_image, (WIDTH - 250, 20))
        display_text(self.screen, f": {self.hero.coins}", WIDTH - 225, 20,
                     (0, 255, 0))

    def open_shop(self):
        """Handle the shop opening logic."""
        shop = Shop(self.hero, self.screen, self.background,
                    self.coin_image)  # Pass the images to the shop
        shop.run()  # Run the shop loop
        self.shop_open = False  # Close the shop after the user exits it

    def start_battle(self):
        """Start a battle between the hero and an enemy."""
        print("Starting battle...")  # Debug print
        # Use the currently displayed enemy (which has the correct level)
        battle_result = battle(self.hero, self.enemy, self.current_level,
                               self.screen, self,
                               self.background)  # Pass background

        if battle_result:
            # Increment stats
            self.enemies_defeated += 1

            # Display victory message
            self.screen.blit(self.background, (0, 0))  # Use background
            display_text(self.screen,
                         f"You defeated the level {self.current_level} enemy!",
                         WIDTH // 2 - 150, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(1000)  # Wait for 1 second

            # Show upgrade menu after victory
            upgrade_menu(self.hero, self.screen, self.background)

            # Give fixed 20 coins after winning
            coins_reward = 20
            self.hero.coins += coins_reward

            # Advance to next level and create a stronger enemy
            self.current_level += 1
            self.enemy = Enemy(level=self.current_level)

            # Make sure the new enemy is positioned on the platform
            land_height = 150
            land_y = HEIGHT - land_height
            self.enemy.y = land_y - 50

            # Display level up message
            self.screen.blit(self.background, (0, 0))  # Use background
            display_text(self.screen,
                         f"Advancing to level {self.current_level}!",
                         WIDTH // 2 - 150, HEIGHT // 2)
            display_text(self.screen,
                         f"Enemy HP: {self.enemy.hp}, Attack: {self.enemy.attack_power}",
                         WIDTH // 2 - 200, HEIGHT // 2 + 40)
            pygame.display.flip()
            pygame.time.delay(1500)  # Show for 1.5 seconds
        else:
            self.game_over()

    def game_over(self):
        """Handle game over state with New Game and Quit buttons."""
        # Create buttons for New Game and Quit
        button_width = 140
        button_height = 50
        button_spacing = 20

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Create button rectangles
        new_game_button = pygame.Rect(
            center_x - button_width - button_spacing // 2,
            center_y + 120,
            button_width,
            button_height
        )

        quit_button = pygame.Rect(
            center_x + button_spacing // 2,
            center_y + 120,
            button_width,
            button_height
        )

        # Prepare font for button text
        font = pygame.font.SysFont(None, 36)
        new_game_text = font.render("New Game", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))

        # Get centered text rects
        new_game_text_rect = new_game_text.get_rect(
            center=new_game_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        while True:
            # Draw game over screen
            self.screen.blit(self.background, (0, 0))  # Use background

            # Center game over texts
            display_text(self.screen, "Game Over", center_x - 60,
                         center_y - 20)
            display_text(self.screen,
                         f"You reached level {self.current_level}",
                         center_x - 100, center_y + 20)
            display_text(self.screen,
                         f"Enemies defeated: {self.enemies_defeated}",
                         center_x - 100, center_y + 60)

            # Draw buttons
            pygame.draw.rect(self.screen, (100, 255, 100),
                             new_game_button)  # Green button
            pygame.draw.rect(self.screen, (255, 100, 100),
                             quit_button)  # Red button

            # Blit centered text onto buttons
            self.screen.blit(new_game_text, new_game_text_rect)
            self.screen.blit(quit_text, quit_text_rect)

            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if new_game_button.collidepoint(mouse_x, mouse_y):
                        self.initialize_game()  # Reset game state
                        return  # Exit game_over and resume run()
                    elif quit_button.collidepoint(mouse_x, mouse_y):
                        self.game_running = False
                        return

            self.clock.tick(60)
