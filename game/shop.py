import pygame
from utils.constants import WIDTH, HEIGHT, WHITE, GREEN
from utils.display import display_text


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
            {"name": "Potion (+25 HP)", "cost": 5, "action": self.buy_potion,
             "image": self.potion_image},
            {"name": "Attack Upgrade (+10 ATK)", "cost": 10,
             "action": self.buy_attack_upgrade, "image": self.sword_image},
            {"name": "Wand Upgrade (+10 Magic ATK)", "cost": 10,
             "action": self.buy_wand_upgrade, "image": self.wand_image},
        ]
        # Add back button
        self.back_button = pygame.Rect(WIDTH - 150, HEIGHT - 50, 100, 40)

    def buy_potion(self):
        """Increase hero HP by 25."""
        self.hero.hp = min(self.hero.max_hp, self.hero.hp + 25)

    def buy_attack_upgrade(self):
        """Increase hero attack by 1."""
        self.hero.strength_level += 1

    def buy_wand_upgrade(self):
        """Increase hero magic attack by 1."""
        self.hero.magic_level += 1

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
                    print(f"Not enough coins to buy {item['name']}.")
        return True

    def render_shop(self):
        """Render the shop menu."""
        # Use background image
        self.screen.blit(self.background, (0, 0))

        # Add a semi-transparent overlay for better readability
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))

        # Shop title
        title_bg = pygame.Rect(WIDTH // 2 - 100, 40, 200, 50)
        pygame.draw.rect(self.screen, (50, 50, 50), title_bg)
        display_text(self.screen, "Shop", WIDTH // 2 - 40, 50)

        # Display Player Stats with background
        stats_bg = pygame.Rect(20, 100, 250, 100)
        pygame.draw.rect(self.screen, (50, 50, 50), stats_bg)

        self.screen.blit(self.hero.health_icon, (30, 120))
        display_text(self.screen, f": {self.hero.hp}/{self.hero.max_hp}", 50,
                     120, GREEN)
        display_text(self.screen, f"Attack: {self.hero.get_attack_power()}",
                     50, 150, GREEN)
        display_text(self.screen,
                     f"Magic Attack: {self.hero.get_magic_power()}", 50, 180,
                     GREEN)

        # Draw coin display with background
        coin_bg = pygame.Rect(WIDTH - 180, 10, 150, 40)
        pygame.draw.rect(self.screen, (50, 50, 50), coin_bg)
        self.screen.blit(self.coin_image, (WIDTH - 170, 20))
        display_text(self.screen, f": {self.hero.coins}", WIDTH - 145, 20,
                     GREEN)

        # Render Shop Items
        self.buttons = []
        y_offset = 250
        for i, item in enumerate(self.shop_items):
            # Create background rectangle for each item
            item_bg = pygame.Rect(WIDTH // 2 - 200, y_offset - 20, 400, 40)
            pygame.draw.rect(self.screen, (50, 50, 50), item_bg)

            # Draw item image (potion, sword, or wand)
            self.screen.blit(item["image"], (WIDTH // 2 - 180, y_offset - 15))

            # Draw item name and cost
            text_surface = self.font.render(
                f"{item['name']} - {item['cost']} coins", True, GREEN)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)

            # Add button detection area
            self.buttons.append((item_bg, item))
            y_offset += 60

        # Draw back button
        pygame.draw.rect(self.screen, (200, 200, 200), self.back_button)
        display_text(self.screen, "Back", WIDTH - 120, HEIGHT - 40)

    def run(self):
        """Run the shop interaction loop."""
        shop_running = True
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
            pygame.time.Clock().tick(60)