# COMP 163: Project 3 - Quest Chronicles

Project Documentation
Module Architecture

character_manager.py
- Handles player characters: create, save/load, validation, XP/leveling, gold, healing, and save-file management. Simple text saves using <name>_save.txt.
inventory.py
- Manages inventory capacity, consumables, equipment, stat effects, shop buying/selling, and item usage via "stat:value" format.
game_data.py
- Loads quests/items from text files, validates formatting, parses block structures, and auto-creates default data if missing.
quest_handler.py
- Controls quest availability, acceptance, completion, prerequisites, progress tracking, XP/gold rewards, and quest lists.
combat_system.py
- Handles enemy creation, turn-based battles, damage, abilities, rewards, win/loss conditions, and combat logs.
main.py
- Central game controller: menus, exploration, shop, saving/loading, character display, running battles, and linking all subsystems into a full playable loop.

Exception Strategy
Your project uses custom errors to enforce correctness and make debugging predictable:
- InventoryFullError — adding items when inventory is at capacity.
- ItemNotFoundError — attempting to remove, use, or sell an item not present.
- InsufficientResourcesError — not enough gold to buy shop items.
- InvalidItemTypeError — invalid item categories or malformed "stat:value" effects.
- MissingDataFileError — required quest/item files are absent.
- InvalidDataFormatError — fields missing or incorrectly formatted in data files.
- CorruptedDataError — parsing fails due to unreadable or damaged content.
- CombatNotActiveError / InvalidTargetError / CharacterDeadError / AbilityOnCooldownError — enforcing legal combat flow and preventing illegal actions mid-battle.

Exceptions are raised as early as possible—during loading, parsing, or validation—to prevent bad data or illegal gameplay states from cascading.

Design Choices
Modular Separation: Inventory, combat, and data loading are isolated so each system can be improved independently.
Text-Based Data Files: Items and quests use human-readable .txt blocks, making the game mod-friendly without changing code.
Stat-Effect Format "stat:value": Simple to parse, allows flexible item/buff definitions, consistent across consumables and equipment.
Turn-Based Combat Loop: Chosen for clarity, readability, and easier debugging.
Clear Validation Steps: Strict parsing avoids silent failures, ensures data integrity, and makes error messages user-friendly.
Equipment Auto-Swap: Equipping returns old gear to inventory automatically to prevent accidental item loss.
Separation of Player Abilities: Special abilities implemented as individual functions for readability and balance tweaking.

AI Usage

AI assistance (ChatGPT) was used for:
Generating module summaries
Refining and debugging strategies.
Drafting readable error explanations and architectural notes.

All game logic, mechanics, and code integration were ultimately created and tested by the developer.
