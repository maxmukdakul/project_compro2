import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox  # Added messagebox import


# Function to read and process CSV files
def read_csv_files():
    # Set the data directory
    data_dir = 'game_data'

    # Read CSV files from the game_data folder
    damage_df = pd.read_csv(os.path.join(data_dir, 'damage.csv'), header=None,
                            names=['session_id', 'timestamp', 'level',
                                   'damage', 'attack_type'])
    health_df = pd.read_csv(os.path.join(data_dir, 'health.csv'), header=None,
                            names=['session_id', 'timestamp', 'level',
                                   'health', 'max_health'])
    items_df = pd.read_csv(os.path.join(data_dir, 'items.csv'), header=None,
                           names=['session_id', 'timestamp', 'level',
                                  'item_name', 'value'])
    skills_df = pd.read_csv(os.path.join(data_dir, 'skills.csv'), header=None,
                            names=['session_id', 'timestamp', 'level',
                                   'skill_name', 'value'])
    upgrades_df = pd.read_csv(os.path.join(data_dir, 'upgrades.csv'),
                              header=None,
                              names=['session_id', 'timestamp', 'level',
                                     'attribute', 'value'])

    return damage_df, health_df, items_df, skills_df, upgrades_df


# Function to create damage graph
def plot_damage_graph(damage_df, ax):
    # Group by level and calculate mean damage
    damage_by_level = damage_df.groupby('level')['damage'].mean().reset_index()

    # Create bar chart
    ax.bar(damage_by_level['level'], damage_by_level['damage'], color='blue',
           alpha=0.7)
    ax.set_xlabel('Level')
    ax.set_ylabel('Average Damage')
    ax.set_title('Average Damage by Level')
    ax.grid(True, linestyle='--', alpha=0.6)

    # Set x-ticks to integer values
    ax.set_xticks(np.unique(damage_df['level']))

    return ax


# Function to create health graph
def plot_health_graph(health_df, ax):
    # Group by level
    health_by_level = health_df.groupby('level').agg({
        'health': 'mean',
        'max_health': 'first'  # All max_health values are the same per level
    }).reset_index()

    # Create line chart
    ax.plot(health_by_level['level'], health_by_level['health'], 'o-',
            color='green', label='Health')
    ax.plot(health_by_level['level'], health_by_level['max_health'], '--',
            color='darkgreen', label='Max Health')
    ax.set_xlabel('Level')
    ax.set_ylabel('Health')
    ax.set_title('Health by Level')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Set x-ticks to integer values
    ax.set_xticks(np.unique(health_df['level']))

    return ax


# Function to create items graph
def plot_items_graph(items_df, ax):
    # Count occurrences of each item
    item_counts = items_df['item_name'].value_counts().reset_index()
    item_counts.columns = ['item_name', 'count']

    # Create horizontal bar chart
    bars = ax.barh(item_counts['item_name'], item_counts['count'],
                   color='purple', alpha=0.7)
    ax.set_xlabel('Count')
    ax.set_ylabel('Item')
    ax.set_title('Item Distribution')
    ax.grid(True, linestyle='--', alpha=0.6, axis='x')

    # Add count labels to the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2,
                f'{width:.0f}',
                ha='left', va='center')

    return ax


# Function to create skills graph
def plot_skills_graph(skills_df, ax):
    # Group by level and skill_name
    skill_by_level = skills_df.groupby(['level', 'skill_name'])[
        'value'].mean().reset_index()

    # Create line chart for each skill
    for skill in skill_by_level['skill_name'].unique():
        skill_data = skill_by_level[skill_by_level['skill_name'] == skill]
        ax.plot(skill_data['level'], skill_data['value'], 'o-', label=skill)

    ax.set_xlabel('Level')
    ax.set_ylabel('Skill Value')
    ax.set_title('Skill Progression by Level')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Set x-ticks to integer values
    ax.set_xticks(np.unique(skills_df['level']))

    return ax


# Function to create upgrades graph
def plot_upgrades_graph(upgrades_df, ax):
    # Group by level and attribute
    upgrades_by_level = upgrades_df.groupby(['level', 'attribute'])[
        'value'].max().reset_index()

    # Create line chart for each attribute
    for attr in upgrades_by_level['attribute'].unique():
        attr_data = upgrades_by_level[upgrades_by_level['attribute'] == attr]
        ax.plot(attr_data['level'], attr_data['value'], 'o-', label=attr)

    ax.set_xlabel('Level')
    ax.set_ylabel('Upgrade Value')
    ax.set_title('Upgrades by Level')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    # Set x-ticks to integer values
    ax.set_xticks(np.unique(upgrades_df['level']))

    return ax


# Function to create correlation graph between damage and upgrades
def plot_correlation_graph(damage_df, upgrades_df, ax):
    # Merge damage and upgrades dataframes on level
    # For each damage entry, find the maximum upgrade value for that level
    damage_level = damage_df.groupby('level')['damage'].mean().reset_index()
    upgrade_level = upgrades_df.groupby('level')['value'].max().reset_index()

    # Fix: Rename columns properly before merging to avoid confusion
    upgrade_level.rename(columns={'value': 'upgrade_value'}, inplace=True)

    merged_df = pd.merge(damage_level, upgrade_level, on='level')

    # Create scatter plot
    ax.scatter(merged_df['upgrade_value'], merged_df['damage'], color='red',
               alpha=0.7)

    # Add trend line
    if len(merged_df) > 1:  # Only add trend line if we have multiple points
        z = np.polyfit(merged_df['upgrade_value'], merged_df['damage'], 1)
        p = np.poly1d(z)
        ax.plot(merged_df['upgrade_value'], p(merged_df['upgrade_value']),
                linestyle='--', color='black', alpha=0.7)

        # Add correlation coefficient
        corr = merged_df['upgrade_value'].corr(merged_df['damage'])
        ax.text(0.05, 0.95, f'Correlation: {corr:.2f}', transform=ax.transAxes)

    ax.set_xlabel('Upgrade Value')
    ax.set_ylabel('Average Damage')
    ax.set_title('Damage vs Upgrade Correlation')
    ax.grid(True, linestyle='--', alpha=0.6)

    return ax


# Function to create the main application
def create_app():
    # Create the main window
    root = tk.Tk()
    root.title("Game Data Visualization")
    root.geometry("1000x700")

    # Try to read the data
    try:
        damage_df, health_df, items_df, skills_df, upgrades_df = read_csv_files()
    except FileNotFoundError as e:
        tk.Label(root, text=f"Error: {e}", fg="red", font=("Arial", 12)).pack(
            pady=20)
        return root

    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    # Create tabs for each graph
    tab_damage = ttk.Frame(notebook)
    tab_health = ttk.Frame(notebook)
    tab_items = ttk.Frame(notebook)
    tab_skills = ttk.Frame(notebook)
    tab_upgrades = ttk.Frame(notebook)
    tab_correlation = ttk.Frame(notebook)

    notebook.add(tab_damage, text='Damage')
    notebook.add(tab_health, text='Health')
    notebook.add(tab_items, text='Items')
    notebook.add(tab_skills, text='Skills')
    notebook.add(tab_upgrades, text='Upgrades')
    notebook.add(tab_correlation, text='Correlation')

    # Create and place the figures and canvases for each tab

    # Damage tab
    fig_damage, ax_damage = plt.subplots(figsize=(8, 5), dpi=100)
    plot_damage_graph(damage_df, ax_damage)
    canvas_damage = FigureCanvasTkAgg(fig_damage, master=tab_damage)
    canvas_damage.draw()
    canvas_damage.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Health tab
    fig_health, ax_health = plt.subplots(figsize=(8, 5), dpi=100)
    plot_health_graph(health_df, ax_health)
    canvas_health = FigureCanvasTkAgg(fig_health, master=tab_health)
    canvas_health.draw()
    canvas_health.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Items tab
    fig_items, ax_items = plt.subplots(figsize=(8, 5), dpi=100)
    plot_items_graph(items_df, ax_items)
    canvas_items = FigureCanvasTkAgg(fig_items, master=tab_items)
    canvas_items.draw()
    canvas_items.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Skills tab
    fig_skills, ax_skills = plt.subplots(figsize=(8, 5), dpi=100)
    plot_skills_graph(skills_df, ax_skills)
    canvas_skills = FigureCanvasTkAgg(fig_skills, master=tab_skills)
    canvas_skills.draw()
    canvas_skills.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Upgrades tab
    fig_upgrades, ax_upgrades = plt.subplots(figsize=(8, 5), dpi=100)
    plot_upgrades_graph(upgrades_df, ax_upgrades)
    canvas_upgrades = FigureCanvasTkAgg(fig_upgrades, master=tab_upgrades)
    canvas_upgrades.draw()
    canvas_upgrades.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Correlation tab
    fig_corr, ax_corr = plt.subplots(figsize=(8, 5), dpi=100)
    plot_correlation_graph(damage_df, upgrades_df, ax_corr)
    canvas_corr = FigureCanvasTkAgg(fig_corr, master=tab_correlation)
    canvas_corr.draw()
    canvas_corr.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add session filter
    session_frame = tk.Frame(root)
    session_frame.pack(fill='x', padx=10, pady=5)

    tk.Label(session_frame, text="Filter by Session:").pack(side='left')

    # Get unique sessions
    sessions = damage_df['session_id'].unique()

    # Create session variable and dropdown
    session_var = tk.StringVar(root)
    session_var.set("All Sessions")  # Default value

    session_dropdown = ttk.Combobox(session_frame, textvariable=session_var)
    session_dropdown['values'] = ['All Sessions'] + list(sessions)
    session_dropdown.pack(side='left', padx=5)

    # Function to update graphs based on session filter
    def update_graphs(*args):
        selected_session = session_var.get()

        # Filter data if a specific session is selected
        if selected_session != "All Sessions":
            filtered_damage = damage_df[
                damage_df['session_id'] == selected_session]
            filtered_health = health_df[
                health_df['session_id'] == selected_session]
            filtered_items = items_df[
                items_df['session_id'] == selected_session]
            filtered_skills = skills_df[
                skills_df['session_id'] == selected_session]
            filtered_upgrades = upgrades_df[
                upgrades_df['session_id'] == selected_session]
        else:
            filtered_damage = damage_df
            filtered_health = health_df
            filtered_items = items_df
            filtered_skills = skills_df
            filtered_upgrades = upgrades_df

        # Clear and redraw each graph
        ax_damage.clear()
        plot_damage_graph(filtered_damage, ax_damage)
        canvas_damage.draw()

        ax_health.clear()
        plot_health_graph(filtered_health, ax_health)
        canvas_health.draw()

        ax_items.clear()
        plot_items_graph(filtered_items, ax_items)
        canvas_items.draw()

        ax_skills.clear()
        plot_skills_graph(filtered_skills, ax_skills)
        canvas_skills.draw()

        ax_upgrades.clear()
        plot_upgrades_graph(filtered_upgrades, ax_upgrades)
        canvas_upgrades.draw()

        ax_corr.clear()
        plot_correlation_graph(filtered_damage, filtered_upgrades, ax_corr)
        canvas_corr.draw()

    # Bind the update function to the dropdown selection
    session_var.trace('w', update_graphs)

    # Add a button to save all graphs
    def save_all_graphs():
        # Create 'graphs' directory if it doesn't exist
        if not os.path.exists('graphs'):
            os.makedirs('graphs')

        # Get the selected session for the filename
        session = session_var.get()
        session_str = session if session != "All Sessions" else "all"

        # Save each figure with session info in filename
        fig_damage.savefig(f'graphs/damage_graph_{session_str}.png')
        fig_health.savefig(f'graphs/health_graph_{session_str}.png')
        fig_items.savefig(f'graphs/items_graph_{session_str}.png')
        fig_skills.savefig(f'graphs/skills_graph_{session_str}.png')
        fig_upgrades.savefig(f'graphs/upgrades_graph_{session_str}.png')
        fig_corr.savefig(f'graphs/correlation_graph_{session_str}.png')

        # Show confirmation
        messagebox.showinfo("Save Complete",
                            "All graphs saved to 'graphs' folder!")

    save_button = tk.Button(session_frame, text="Save All Graphs",
                            command=save_all_graphs)
    save_button.pack(side='right', padx=5)

    return root


# Main function
def main():
    # Check if game_data directory exists
    if not os.path.exists('game_data'):
        print("Error: 'game_data' directory not found!")
        print(
            "Please make sure your CSV files are in a folder named 'game_data'")
        input("Press Enter to exit...")
        return

    app = create_app()
    # Adjust figure styles globally
    plt.style.use('seaborn-v0_8-darkgrid')
    app.mainloop()


if __name__ == "__main__":
    main()