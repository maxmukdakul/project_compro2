import csv
import os
from datetime import datetime


class DataCollector:
    def __init__(self):
        """Initialize the data collector for tracking game statistics."""
        self.data_dir = "game_data"

        # Ensure game_data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # CSV file paths
        self.skills_file = os.path.join(self.data_dir, "skills.csv")
        self.upgrades_file = os.path.join(self.data_dir, "upgrades.csv")
        self.damage_file = os.path.join(self.data_dir, "damage.csv")
        self.health_file = os.path.join(self.data_dir, "health.csv")
        self.items_file = os.path.join(self.data_dir, "items.csv")

        # Initialize each file with headers if they don't exist
        self._initialize_files()

        # Track current game session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def _initialize_files(self):
        """Create CSV files with headers if they don't exist."""
        # Skills data
        if not os.path.exists(self.skills_file):
            with open(self.skills_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['session_id', 'timestamp', 'floor', 'skill_name',
                     'effect'])

        # Upgrades data
        if not os.path.exists(self.upgrades_file):
            with open(self.upgrades_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['session_id', 'timestamp', 'floor', 'stat_upgraded',
                     'new_value'])

        # Damage data
        if not os.path.exists(self.damage_file):
            with open(self.damage_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['session_id', 'timestamp', 'floor', 'damage_dealt',
                     'attack_type'])

        # Health data
        if not os.path.exists(self.health_file):
            with open(self.health_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['session_id', 'timestamp', 'floor', 'health_remaining',
                     'max_health'])

        # Items data
        if not os.path.exists(self.items_file):
            with open(self.items_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['session_id', 'timestamp', 'floor', 'item_name', 'cost'])

    def track_skill_use(self, floor, skill_name, effect):
        """Track when a skill is used.

        Args:
            floor: Current floor/level of the game
            skill_name: Name of the skill used (e.g., "Magic Attack", "Heal")
            effect: Effect of the skill (e.g., damage dealt, health restored)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.skills_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [self.session_id, timestamp, floor, skill_name, effect])

    def track_upgrade(self, floor, stat_upgraded, new_value):
        """Track when a character stat is upgraded.

        Args:
            floor: Current floor/level of the game
            stat_upgraded: Name of the stat upgraded (e.g., "Strength", "Magic", "Speed", "Health")
            new_value: New value of the stat after upgrade
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.upgrades_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [self.session_id, timestamp, floor, stat_upgraded, new_value])

    def track_damage(self, floor, damage_dealt, attack_type):
        """Track damage dealt to enemies.

        Args:
            floor: Current floor/level of the game
            damage_dealt: Amount of damage dealt
            attack_type: Type of attack (e.g., "Magic", "Strength")
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.damage_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [self.session_id, timestamp, floor, damage_dealt, attack_type])

    def track_health(self, floor, health_remaining, max_health):
        """Track player health at the end of each floor.

        Args:
            floor: Current floor/level of the game
            health_remaining: Health points remaining after the floor
            max_health: Maximum health of the player
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.health_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [self.session_id, timestamp, floor, health_remaining,
                 max_health])

    def track_item_purchase(self, floor, item_name, cost):
        """Track items purchased from the shop.

        Args:
            floor: Current floor/level of the game
            item_name: Name of the item purchased
            cost: Cost of the item in coins
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.items_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [self.session_id, timestamp, floor, item_name, cost])


# Create a singleton instance of the DataCollector
collector = DataCollector()


# Utility functions for easier access from other modules
def track_skill_use(floor, skill_name, effect):
    collector.track_skill_use(floor, skill_name, effect)


def track_upgrade(floor, stat_upgraded, new_value):
    collector.track_upgrade(floor, stat_upgraded, new_value)


def track_damage(floor, damage_dealt, attack_type):
    collector.track_damage(floor, damage_dealt, attack_type)


def track_health(floor, health_remaining, max_health):
    collector.track_health(floor, health_remaining, max_health)


def track_item_purchase(floor, item_name, cost):
    collector.track_item_purchase(floor, item_name, cost)