"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Kabijah

AI Usage: Made ChatGPT give me testing stuff

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError

    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file '{filename}' not found.")

    try:
        quests = {}
        with open(filename, "r") as f:
            block = []
            for line in f:
                if line.strip() == "":
                    if block:
                        quest = parse_quest_block(block)
                        validate_quest_data(quest)
                        quests[quest["quest_id"]] = quest
                        block = []
                else:
                    block.append(line.strip())

            # Catch last block if no trailing newline
            if block:
                quest = parse_quest_block(block)
                validate_quest_data(quest)
                quests[quest["quest_id"]] = quest

        return quests

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not parse quest data: {e}")
    pass

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file '{filename}' not found.")

    try:
        items = {}
        with open(filename, "r") as f:
            block = []
            for line in f:
                if line.strip() == "":
                    if block:
                        item = parse_item_block(block)
                        validate_item_data(item)
                        items[item["item_id"]] = item
                        block = []
                else:
                    block.append(line.strip())

            if block:
                item = parse_item_block(block)
                validate_item_data(item)
                items[item["item_id"]] = item

        return items

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not parse item data: {e}")
        pass

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level",
        "prerequisite"
    ]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing field: {key}")

    # Numeric checks
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]

    for num in numeric_fields:
        if not isinstance(quest_dict[num], int):
            raise InvalidDataFormatError(f"Expected integer for {num}")

    return True
    pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    valid_types = {"weapon", "armor", "consumable"}
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer.")

    # EFFECT format: "stat:value"
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("Invalid effect format. Expected stat:value")

    stat, value = item_dict["effect"].split(":", 1)
    if not value.isdigit():
        raise InvalidDataFormatError("Item effect value must be an integer.")

    return True
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    """Creates data folder + starter files if missing."""
    os.makedirs("data", exist_ok=True)

    # Default quests
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f:
            f.write(
                "QUEST_ID: first_steps\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Your journey begins!\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 10\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n\n"
            )

    # Default items
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w") as f:
            f.write(
                "ITEM_ID: potion_basic\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:25\n"
                "COST: 20\n"
                "DESCRIPTION: Restores 25 HP.\n\n"
            )

    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}
    expected_fields = {
        "QUEST_ID": "quest_id",
        "TITLE": "title",
        "DESCRIPTION": "description",
        "REWARD_XP": "reward_xp",
        "REWARD_GOLD": "reward_gold",
        "REQUIRED_LEVEL": "required_level",
        "PREREQUISITE": "prerequisite"
    }

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid line format: {line}")

        key, value = line.split(": ", 1)

        if key not in expected_fields:
            raise InvalidDataFormatError(f"Unexpected quest field: {key}")

        mapped_key = expected_fields[key]

        # Convert numeric fields
        if mapped_key in ["reward_xp", "reward_gold", "required_level"]:
            if not value.isdigit():
                raise InvalidDataFormatError(f"Expected number for {key}")
            value = int(value)

        quest[mapped_key] = value

    return quest
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}
    expected_fields = {
        "ITEM_ID": "item_id",
        "NAME": "name",
        "TYPE": "type",
        "EFFECT": "effect",
        "COST": "cost",
        "DESCRIPTION": "description"
    }

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid item line: {line}")

        key, value = line.split(": ", 1)

        if key not in expected_fields:
            raise InvalidDataFormatError(f"Unexpected item field: {key}")

        mapped_key = expected_fields[key]

        if mapped_key == "cost":
            if not value.isdigit():
                raise InvalidDataFormatError("Item cost must be a number.")
            value = int(value)

        item[mapped_key] = value

    return item
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    print("\n[STEP 1] Checking/creating default data files...")
    try:
        create_default_data_files()
        print("Default data files ready ✔")
    except Exception as e:
        print(f"FAILED: Could not create default files: {e}")

    # ----------------------------------
    # 2. Test loading quests
    # ----------------------------------
    print("\n[STEP 2] Testing quest loading...")
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quest(s) ✔")
        for qid, q in quests.items():
            print(f" - {qid}: {q['title']} (XP: {q['reward_xp']})")
    except MissingDataFileError:
        print("FAILED: quests.txt is missing!")
    except InvalidDataFormatError as e:
        print(f"FAILED: Quest format error → {e}")
    except CorruptedDataError as e:
        print(f"FAILED: Quest data corrupted → {e}")

    # ----------------------------------
    # 3. Test loading items
    # ----------------------------------
    print("\n[STEP 3] Testing item loading...")
    try:
        items = load_items()
        print(f"Loaded {len(items)} item(s) ✔")
        for iid, item in items.items():
            print(f" - {iid}: {item['name']} ({item['type']})")
    except MissingDataFileError:
        print("FAILED: items.txt is missing!")
    except InvalidDataFormatError as e:
        print(f"FAILED: Item format error → {e}")
    except CorruptedDataError as e:
        print(f"FAILED: Item data corrupted → {e}")

    print("\n=== SELF-TEST COMPLETE ===")

