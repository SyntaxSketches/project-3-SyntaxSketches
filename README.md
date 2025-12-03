# COMP 163: Project 3 - Quest Chronicles

Project Documentation
Module Architecture
inventory.py — Manages player inventory, consumables, equipment, and shop actions. Includes item usage, gear swapping, stat-effect parsing, and shop purchase/sell logic.
data_loader.py — Loads and validates quest and item data from text files. Auto-generates default data if missing. Handles parsing of item/quest blocks and strict format checking.
combat_system.py — Handles enemy creation, turn-based combat, attacks, abilities, damage calculations, rewards, and combat logging.
character.py (implied) — Defines player stats, classes, and health cap logic used across modules.
main.py / game.py (or equivalent) — High-level game loop that connects exploration, combat, inventory, and progression.

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
