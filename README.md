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
- Keep things separate: Inventory, combat, and data loading all run on their own, so it’s easier to tweak or upgrade each without messing up the others.
- Simple text files: Items and quests are stored in plain .txt files, which makes modding super easy without touching the actual code.
- Easy stat format: Using "stat:value" keeps things consistent and flexible for buffs, consumables, and gear.
- Turn-based battles: The combat loop is turn-based, which makes it clearer to follow and way easier to debug.
- Strict checks: Data gets validated carefully, so you don’t end up with silent errors—plus, error messages are straightforward.
- Auto gear swap: When you equip something new, your old gear goes back into your inventory automatically, so nothing gets lost.
- Abilities split up: Special abilities are written as separate functions, which keeps the code clean and makes balancing simpler.

AI Usage
- AI assistance (ChatGPT) was used for:
- Generating module summaries
- Refining and debugging strategies.
- Drafting readable error explanations and architectural notes.
