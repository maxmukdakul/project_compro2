import pygame
from utils.constants import WIDTH, HEIGHT, WHITE, GREEN
from utils.display import display_text
import data_collector


class Shop:
    def __init__(self, hero, screen, background, coin_image):
        self.hero = hero
        self.screen = screen
        self.background = background
        self.coin_image = coin_image
        self.font = pygame.font.Font(None, 36)

        # Load potion image
        self.potion_image = pygame.image.load('images/potion.png')
        self.potion_image = pygame.transform.scale(self.potion_image, (30, 30))

        # Load other item images
        self.sword_image = pygame.image.load('images/sword.png')
        self.sword_image = pygame.transform.scale(self.sword_image, (30, 30))

        self.wand_image = pygame.image.load('images/wand.png')
        self.wand_image = pygame.transform.scale(self.wand_image, (30, 30))

        self.shop_items = [
            {"name": "Potion (+25 HP)", "cost": 15, "action": self.buy_potion,
             "image": self.potion_image},
            {"name": "Sword (+10 ATK)", "cost": 20,
             "action": self.buy_attack_upgrade, "image": self.sword_image},
            {"name": "Wand (+10 Magic)", "cost": 20,
             "action": self.buy_wand_upgrade, "image": self.wand_image},
        ]
        # Add back button
        self.back_button = pygame.Rect(WIDTH - 150, HEIGHT - 50, 100, 40)

        # Create a purchase message system
        self.message = ""
        self.message_timer = 0
        self.message_duration = 120  # 2 seconds at 60fps

    def buy_potion(self):
        """Increase hero HP by 25."""
        self.hero.hp = min(self.hero.max_hp, self.hero.hp + 25)
        self.show_message("Potion purchased! +25 HP")
        # Track the purchase
        data_collector.track_item_purchase(self.hero.current_level, "Potion (+25 HP)", 15)

    def buy_attack_upgrade(self):
        """Increase hero attack by 1."""
        self.hero.strength_level += 1
        self.show_message("Attack upgraded! +10 ATK")
        # Track the purchase
        data_collector.track_item_purchase(self.hero.current_level, "Sword (+10 ATK)", 20)

    def buy_wand_upgrade(self):
        """Increase hero magic attack by 1."""
        self.hero.magic_level += 1
        self.show_message("Magic upgraded! +10 Magic ATK")
        # Track the purchase
        data_collector.track_item_purchase(self.hero.current_level, "Wand (+10 Magic)", 20)

    def show_message(self, text):
        """Display a purchase message."""
        self.message = text
        self.message_timer = self.message_duration

    def handle_button_click(self, mouse_x, mouse_y):
        """Handle button clicks to buy items."""
        # Check for back button first
        if self.back_button.collidepoint(mouse_x, mouse_y):
            return False  # Signal to exit the shop

        for button, item in self.buttons:
            if button.collidepoint(mouse_x, mouse_y):
                if self.hero.coins >= item["cost"]:
                    self.hero.coins -= item["cost"]
                    item["action"]()  # Call the specific item effect
                else:
                    self.show_message(f"Not enough coins for {item['name']}!")
        return True

    def render_shop(self):
        """Render the shop menu."""
        # Use background image
        self.screen.blit(self.background, (0, 0))

        # Add a semi-transparent overlay for better readability
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # More opaque black
        self.screen.blit(overlay, (0, 0))

        # Shop title - larger and more prominent
        title_bg = pygame.Rect(WIDTH // 2 - 150, 40, 300, 60)
        pygame.draw.rect(self.screen, (50, 50, 50), title_bg, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 100), title_bg, 3,
                         border_radius=10)  # Border
        display_text(self.screen, "Shop", WIDTH // 2 - 40, 55, font_size=48)

        # Display Player Stats with better background
        stats_bg = pygame.Rect(20, 100, 250, 120)
        pygame.draw.rect(self.screen, (50, 50, 50), stats_bg, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), stats_bg, 2,
                         border_radius=8)  # Border

        self.screen.blit(self.hero.health_icon, (30, 120))
        display_text(self.screen, f": {self.hero.hp}/{self.hero.max_hp}", 50,
                     120, GREEN)
        display_text(self.screen, f"Attack: {self.hero.get_attack_power()}",
                     50, 150, GREEN)
        display_text(self.screen,
                     f"Magic Attack: {self.hero.get_magic_power()}", 50, 180,
                     GREEN)

        # Draw coin display with nicer background
        coin_bg = pygame.Rect(WIDTH - 180, 10, 150, 40)
        pygame.draw.rect(self.screen, (50, 50, 50), coin_bg, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), coin_bg, 2,
                         border_radius=8)  # Border
        self.screen.blit(self.coin_image, (WIDTH - 170, 20))
        display_text(self.screen, f": {self.hero.coins}", WIDTH - 145, 20,
                     GREEN)

        # Render Shop Items
        self.buttons = []
        y_offset = 250

        # Create shop items panel
        items_panel = pygame.Rect(WIDTH // 2 - 225, 230, 450, 250)
        pygame.draw.rect(self.screen, (40, 40, 40), items_panel,
                         border_radius=12)
        pygame.draw.rect(self.screen, (100, 100, 100), items_panel, 2,
                         border_radius=12)  # Border

        # Add a header for better organization
        header_start_x = WIDTH // 2 - 190
        price_x = WIDTH // 2 + 100
        display_text(self.screen, "Item", header_start_x, y_offset - 30,
                     (200, 200, 200))
        display_text(self.screen, "Price", price_x, y_offset - 30,
                     (200, 200, 200))

        for i, item in enumerate(self.shop_items):
            # Create button for each item
            item_bg = pygame.Rect(WIDTH // 2 - 200, y_offset, 400, 50)

            # Change button color on hover
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if item_bg.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.screen, (70, 70, 70), item_bg,
                                 border_radius=8)
            else:
                pygame.draw.rect(self.screen, (50, 50, 50), item_bg,
                                 border_radius=8)

            pygame.draw.rect(self.screen, (100, 100, 100), item_bg, 2,
                             border_radius=8)  # Border

            # Draw item image with proper alignment
            image_x = WIDTH // 2 - 190
            image_y = y_offset + 10
            self.screen.blit(item["image"], (image_x, image_y))

            # Draw item name - aligned to the left
            display_text(self.screen, f"{item['name']}", WIDTH // 2 - 150,
                         y_offset + 25, GREEN)

            # Draw cost - fixed position on the right side
            display_text(self.screen, f"{item['cost']} coins",
                         WIDTH // 2 + 100, y_offset + 25, GREEN)

            # Add button detection area
            self.buttons.append((item_bg, item))
            y_offset += 70

        # Draw back button with better styling
        back_button_bg = pygame.Rect(WIDTH - 150, HEIGHT - 50, 100, 40)
        pygame.draw.rect(self.screen, (60, 60, 60), back_button_bg,
                         border_radius=8)
        pygame.draw.rect(self.screen, (120, 120, 120), back_button_bg, 2,
                         border_radius=8)  # Border
        display_text(self.screen, "Back", WIDTH - 120, HEIGHT - 40)

        # Display purchase message if there is one
        if self.message_timer > 0:
            message_bg = pygame.Rect(WIDTH // 2 - 200, HEIGHT - 100, 400, 50)
            pygame.draw.rect(self.screen, (50, 100, 50), message_bg,
                             border_radius=10)
            pygame.draw.rect(self.screen, (100, 200, 100), message_bg, 2,
                             border_radius=10)
            display_text(self.screen, self.message,
                         WIDTH // 2 - len(self.message) * 8, HEIGHT - 85,
                         WHITE)
            self.message_timer -= 1

    def run(self):
        """Run the shop interaction loop."""
        shop_running = True
        clock = pygame.time.Clock()

        while shop_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    shop_running = self.handle_button_click(mouse_x, mouse_y)

            self.render_shop()
            pygame.display.flip()
            clock.tick(60)