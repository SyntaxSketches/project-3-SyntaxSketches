"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Complete Code

Name: Kabijah Hill
AI Usage: Fixed structure, improved errors, cleaned validation.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER CREATION
# ============================================================================

def create_character(name, character_class):

    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }
    
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    base = valid_classes[character_class]

    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ============================================================================
# SAVE CHARACTER
# ============================================================================

def save_character(character, save_directory="data/save_games"):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    with open(filename, "w") as f:
        for key in [
            "name", "class", "level", "health", "max_health",
            "strength", "magic", "experience", "gold"
        ]:
            f.write(f"{key.upper()}: {character[key]}\n")

        f.write("INVENTORY: " + ",".join(character["inventory"]) + "\n")
        f.write("ACTIVE_QUESTS: " + ",".join(character["active_quests"]) + "\n")
        f.write("COMPLETED_QUESTS: " + ",".join(character["completed_quests"]) + "\n")

    return True

# ============================================================================
# LOAD CHARACTER
# ============================================================================

def load_character(character_name, save_directory="data/save_games"):

    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} not found")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        raise SaveFileCorruptedError("Could not read save file")

    data = {}

    try:
        for line in lines:
        clean = line.strip()
        if clean == "":
            continue  # skip blank lines

        if ": " not in clean:
            raise InvalidSaveDataError("Bad save file formatting")

        key, value = clean.split(": ", 1)

            if key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                data[key.lower()] = value.split(",") if value else []
            elif key in ["LEVEL","HEALTH","MAX_HEALTH","STRENGTH","MAGIC","EXPERIENCE","GOLD"]:
                data[key.lower()] = int(value)
            else:
                data[key.lower()] = value
    except Exception:
        raise InvalidSaveDataError("Bad save file formatting")

    validate_character_data(data)
    return data

# ============================================================================
# LIST / DELETE SAVES
# ============================================================================

def list_saved_characters(save_directory="data/save_games"):

    if not os.path.exists(save_directory):
        return []

    return [
        filename.replace("_save.txt", "")
        for filename in os.listdir(save_directory)
        if filename.endswith("_save.txt")
    ]


def delete_character(character_name, save_directory="data/save_games"):

    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} does not exist")

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):

    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead")

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return character


def add_gold(character, amount):

    if character["gold"] + amount < 0:
        raise ValueError("Not enough gold")

    character["gold"] += amount
    return character["gold"]


def heal_character(character, amount):

    before = character["health"]
    character["health"] = min(character["max_health"], character["health"] + amount)
    return character["health"] - before


def is_character_dead(character):
    return character["health"] <= 0


def revive_character(character):

    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):

    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    numeric = ["level","health","max_health","strength","magic","experience","gold"]
    for n in numeric:
        if type(character[n]) is not int:
            raise InvalidSaveDataError(f"{n} must be int")

    for l in ["inventory","active_quests","completed_quests"]:
        if type(character[l]) is not list:
            raise InvalidSaveDataError(f"{l} must be list")

    return True

# ============================================================================
# TESTING SUITE
# ============================================================================

if __name__ == "__main__":

    print("\n=== CHARACTER MANAGER TEST SUITE ===")

    # 1) CREATE
    try:
        hero = create_character("TestHero", "Warrior")
        print("Create OK:", hero)
    except Exception as e:
        print("Create FAILED:", e)

    # 2) SAVE
    try:
        save_character(hero)
        print("Save OK")
    except Exception as e:
        print("Save FAILED:", e)

    # 3) LOAD
    try:
        loaded = load_character("TestHero")
        print("Load OK:", loaded)
    except Exception as e:
        print("Load FAILED:", e)

    # 4) XP & LEVEL
    print("\n-- XP Level Test --")
    hero = gain_experience(hero, 250)
    print("After XP:", hero)

    # 5) GOLD
    print("\n-- Gold Test --")
    try:
        print("New Gold:", add_gold(hero, 50))
    except Exception as e:
        print("Gold Error:", e)

    # 6) HEALING
    print("\n-- Heal Test --")
    hero["health"] = 10
    healed = heal_character(hero, 30)
    print(f"Healed {healed}, now {hero['health']}")

    # 7) REVIVE
    print("\n-- Revival Test --")
    hero["health"] = 0
    revive_character(hero)
    print("Revived:", hero["health"])

    # 8) LIST SAVES
    print("\n-- List Saves --")
    print(list_saved_characters())

    # 9) DELETE SAVE
    print("\n-- Delete TestHero --")
    delete_character("TestHero")
    print("Deleted OK")

    print("\n=== ALL TESTS COMPLETE ===")

