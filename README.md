# Project Compro2

## Overview
Project Compro2 is a Python-based game that combines engaging gameplay mechanics with a robust data visualization tool. The project is designed using object-oriented principles and includes features such as battling enemies, upgrading characters, and analyzing gameplay performance.

---

## Prerequisites
Before running the project, ensure you have the following installed:

1. **Python 3.8+**
2. **Dependencies**:
   - `pygame`: For game development.
   - `pandas`: For data processing.
   - `matplotlib`: For creating visualizations.
   - `numpy`: For numerical operations.

To install these dependencies, run the following command:
```bash
pip install -r requirements.txt
```
## How to Run the Game
1. Clone this repo
https://github.com/maxmukdakul/project_compro2.git
2. Navigate to the root directory of the project:
```bash
cd project_compro2
```
3. Run the main game file:
```bash
python main.py
```
4. The game window will open. Follow on-screen instructions to play the game.


## How to Run the Graph Visualization
The graph visualization tool is used to analyze game data stored in CSV files under the game_data directory.

1. Ensure the game_data directory contains the following CSV files:

   - `damage.csv`: Tracks damage statistics.
   - `health.csv`: Tracks health metrics.
   - `skills.csv`: Tracks skills usage.
   - `items.csv`: Tracks purchased items.
   - `upgrades.csv`: Tracks upgrades made during the game.
2. Run the visualization tool:

```bash
python game_visualization.py
```
3. A GUI window will open, allowing you to view graphs for:

- Damage
- Health
- Items
- Skills
- Upgrades
- Correlation between damage and upgrades
4. Use the dropdown menu to filter data by session or view all sessions.

5. To save all graphs, click the "Save All Graphs" button in the GUI.

## Notes
Ensure the game_data directory exists in the root folder and contains valid CSV data before running the graph visualization tool.
The game saves data automatically during gameplay, which will be available for visualization.
