"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Kabijah H

AI Usage: debugging and code structure

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    while True:
        choice = input("Choose an option (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print("Invalid choice. Enter 1-3.")
    pass

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    print("\n=== NEW GAME ===")
    name = input("Enter your character name: ").strip()

    print("\nChoose your class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_map = {"1": "Warrior", "2": "Mage", "3": "Rogue", "4": "Cleric"}

    while True:
        c_choice = input("Choose class (1-4): ").strip()
        if c_choice in class_map:
            char_class = class_map[c_choice]
            break
        print("Invalid choice. Enter 1-4.")

    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"\nCharacter '{name}' the {char_class} created!")
    except InvalidCharacterClassError as e:
        print(f"Error: {e}")
        return

    game_loop()
    pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    print("\n=== LOAD GAME ===")
    saves = character_manager.list_saved_characters()

    if not saves:
        print("No saved games found.")
        return

    print("\nSaved Characters:")
    for i, name in enumerate(saves, 1):
        print(f"{i}. {name}")

    while True:
        try:
            choice = int(input("Select character number: "))
            if 1 <= choice <= len(saves):
                break
        except ValueError:
            pass
        print("Invalid input.")

    try:
        current_character = character_manager.load_character(saves[choice - 1])
        print("\nGame loaded successfully!")
        game_loop()

    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading game: {e}")
    pass

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    game_running = True
    
    print("\n=== ENTERING GAME WORLD ===")

    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved! Exiting to main menu.\n")
            break
    pass

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Battle!)")
    print("5. Shop")
    print("6. Save and Quit")

    while True:
        choice = input("Choose an option (1-6): ").strip()
        if choice in ("1", "2", "3", "4", "5", "6"):
            return int(choice)
        print("Invalid choice. Enter 1-6.")
    pass

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("\n=== CHARACTER STATS ===")
    character_manager.display_character_stats(current_character)

    print("\nQuest Progress:")
    quest_handler.display_quest_progress(current_character, all_quests)
    pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character)

    print("\nOptions:")
    print("1. Use Item")
    print("2. Equip Item")
    print("3. Drop Item")
    print("4. Back")

    choice = input("Choose (1-4): ").strip()

    if choice == "1":
        item = input("Item to use: ").strip()
        try:
            inventory_system.use_item(current_character, item)
            print(f"Used {item}!")
        except InventoryError as e:
            print(f"Error: {e}")

    elif choice == "2":
        item = input("Item to equip: ").strip()
        try:
            inventory_system.equip_item(current_character, item)
            print(f"Equipped {item}!")
        except InventoryError as e:
            print(f"Error: {e}")

    elif choice == "3":
        item = input("Item to drop: ").strip()
        try:
            inventory_system.drop_item(current_character, item)
            print(f"Dropped {item}.")
        except InventoryError as e:
            print(f"Error: {e}")
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    print("\n=== QUEST MENU ===")
    print("1. Active Quests")
    print("2. Available Quests")
    print("3. Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (TESTING)")
    print("7. Back")

    choice = input("Choose (1-7): ").strip()

    if choice == "1":
        quest_handler.show_active_quests(current_character, all_quests)
    elif choice == "2":
        quest_handler.show_available_quests(all_quests)
    elif choice == "3":
        quest_handler.show_completed_quests(current_character)
    elif choice == "4":
        quest_name = input("Quest to accept: ").strip()
        try:
            quest_handler.accept_quest(current_character, quest_name, all_quests)
            print("Quest accepted!")
        except QuestError as e:
            print(f"Error: {e}")
    elif choice == "5":
        quest_name = input("Quest to abandon: ").strip()
        try:
            quest_handler.abandon_quest(current_character, quest_name)
            print("Quest abandoned.")
        except QuestError as e:
            print(f"Error: {e}")
    elif choice == "6":
        q = input("Quest to force-complete: ").strip()
        try:
            quest_handler.complete_quest(current_character, q, all_quests)
            print("Quest completed! (Test Mode)")
        except QuestError as e:
            print(f"Error: {e}")

    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    print("\n=== EXPLORING... ===")
    level = current_character["level"]
    enemy = combat_system.get_random_enemy_for_level(level)

    print(f"A wild {enemy['name']} appears!")
    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()

        if result["winner"] == "player":
            print("\nYou won the battle!")
            print(f"Gained {result['xp_gained']} XP and {result['gold_gained']} gold!")
            character_manager.add_xp(current_character, result["xp_gained"])
            current_character["gold"] += result["gold_gained"]

        elif result["winner"] == "enemy":
            print("\nYou have been defeated...")
            handle_character_death()

    except CharacterDeadError:
        print("You died before the battle began!")
        handle_character_death()
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    print("\n=== SHOP ===")
    print(f"Your Gold: {current_character['gold']}")
    game_data.display_shop_items(all_items)

    print("\nOptions:")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back")

    choice = input("Choose (1-3): ").strip()

    if choice == "1":
        item = input("Item to buy: ").strip()
        try:
            inventory_system.buy_item(current_character, item, all_items)
            print(f"Bought {item}!")
        except InventoryError as e:
            print(f"Error: {e}")

    elif choice == "2":
        item = input("Item to sell: ").strip()
        try:
            inventory_system.sell_item(current_character, item, all_items)
            print(f"Sold {item}.")
        except InventoryError as e:
            print(f"Error: {e}") 
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Save failed: {e}")
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Missing data file — creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Data error: {e}")
        raise
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    print("\n=== YOU DIED ===")
    print("1. Revive (Cost: 20 gold)")
    print("2. Quit to Main Menu")

    choice = input("Choose (1-2): ").strip()

    if choice == "1":
        try:
            character_manager.revive_character(current_character)
            print("You have been revived!")
        except InsufficientGoldError as e:
            print(f"Error: {e}")
            game_running = False
    else:
        game_running = False
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

