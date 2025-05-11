# Tower Climbing Game

## Project Overview

### Game Flow Enhancements

#### Battle Phase
The turn-based battle system includes defined actions such as Magic Attack, Strength Attack, Defend, and Heal.  
**Proposed Improvement:** Introduce status effects like poison and freeze to add strategic depth to combat.

#### Reward & Upgrade Phase
Players earn coins and upgrade stats between battles.  
**Proposed Improvement:** Implement a dynamic scaling system where higher levels offer greater rewards but also increase upgrade costs.

---

## Project Review

### Closest Reference Projects
- **Pokémon**
- **Tower Climbing**

### Planned Improvements

- **Integrated Battle System:**  
  Add attack animations and visual effects to enhance engagement.

- **Reward Mechanism:**  
  Introduce rare item drops such as healing potions and temporary buffs.

- **Attribute Upgrades:**  
  Enable hybrid upgrades (e.g., +0.5 Strength and +5 HP) for flexible stat progression.

- **Shop System:**  
  Add a rotating inventory system with dynamically changing stock.

- **Enhanced Gameplay Loop:**  
  Include random events between levels such as mini-games and treasure hunts for added variety.

---

## Programming Development

### 3.1 Game Concept

The game follows a cycle:

1. **Battle Phase**:  
   Players engage in turn-based combat, choosing physical or magical attacks. Monsters retaliate with their own moves.

2. **Reward & Upgrade Phase**:  
   Players gain coins and level up. Between battles, they visit the shop to purchase upgrades for:
   - **Strength** (+1): Physical damage
   - **Magic** (+1): Magic damage
   - **Speed** (+0.1): Turn priority, dodge rate
   - **Health** (+50): Max HP

3. **Repeat**:  
   Players climb to the next tower level with improved stats.

---

### 3.2 Object-Oriented Programming Implementation

| Class         | Role                             | Attributes                        | Methods                                                  |
|---------------|----------------------------------|-----------------------------------|----------------------------------------------------------|
| Game          | Controls game states and flow    | state, screen, clock              | run(), switch_state(), handle_events(), start_battle()  |
| Player        | Represents the main character     | hp, level, coins, stats           | attack_magic(), attack_strength(), heal(), defend()     |
| Monster       | Enemy character in battles        | hp, attack_power, level           | choose_move(), receive_damage(), attack()               |
| BattleSystem  | Manages turn-based combat         | turn_order, battle_log            | start_battle(), apply_damage(), end_battle()            |
| Shop          | Handles in-game purchases         | inventory, item_costs             | display_shop(), purchase_item(), apply_upgrade()        |

---

### 3.3 Algorithms Involved

- **Turn-Based Battle Algorithm**:
  - Determines turn order using the speed stat.
  - Calculates damage using stats and random modifiers.
  - Ends battle when one character's HP reaches zero.

- **EXP and Coin Rewards**:
  - Rewards scale with enemy difficulty.
  - Leveling up increases base stats and may unlock new abilities.

- **Upgrade & Shop System**:
  - Shop sells potions, weapons, and magic tools.
  - Includes affordability checks.
  - Example items:
    - **Potion**: +25 HP
    - **Sword**: +10 Strength
    - **Wand**: +10 Magic

- **Event-Driven Input Processing**:
  - Inputs are managed through a validated event loop.
  - Ensures accurate and responsive gameplay transitions.

---

## Statistical Data Collection

### 4.1 Data Features

| Feature                | Purpose                                             | Source (CSV)             | Visualization           |
|------------------------|-----------------------------------------------------|--------------------------|-------------------------|
| Damage Metrics         | Analyze average damage, accuracy, and attack types  | `damage.csv`             | Bar chart               |
| Health Metrics         | Track HP progression per level                      | `health.csv`             | Line graph              |
| Item Usage             | Evaluate item dependency and frequency              | `items.csv`              | Table                   |
| Skill Effectiveness    | Measure skill frequency and outcome                 | `skills.csv`             | Line graph              |
| Upgrades & Transactions| Track upgrades and purchases                        | `upgrades.csv`           | Table                   |

---

### 4.2 Data Recording Method

Data is recorded in `.csv` format using a `DataCollector` class, facilitating easy analysis with Python tools such as pandas and matplotlib.

- **Damage Data**: Logs attack type, damage, and outcomes.
- **Health Data**: Tracks current vs. max HP after each level.
- **Item Data**: Logs item purchases and in-battle usage.
- **Skill Data**: Tracks frequency and results of skill usage.
- **Upgrade Data**: Logs upgrade choices and shop purchases with associated costs.

---

### 4.3 Data Analysis Report

**Insights Generated**:

- **Damage Analysis**: Average damage per skill, usage frequency, accuracy.
- **Health Trends**: Health lost per level, recovery efficiency.
- **Item Use**: Reliance on potions or buffs, impact on win rate.
- **Skill Analysis**: Most effective skills, usage patterns.
- **Upgrade & Economy Trends**: Popular upgrade paths, item affordability, shop balance.

**Visualization Tools**:
- Bar charts for skill and damage metrics.
- Line graphs for health and skill progression.
- Tables for item usage and upgrade logs.

---

**UML**
