"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Kabijah 

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    enemy_type = enemy_type.lower()

    enemy_stats = {
        "goblin":  {"health": 50,  "strength": 8,  "magic": 2,  "xp": 25,  "gold": 10},
        "orc":     {"health": 80,  "strength": 12, "magic": 5,  "xp": 50,  "gold": 25},
        "dragon":  {"health": 200, "strength": 25, "magic": 15, "xp": 200, "gold": 100}
    }

    if enemy_type not in enemy_stats:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' is not recognized.")

    base = enemy_stats[enemy_type]
     
    return {
        "name": enemy_type.capitalize(),
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "xp_reward": base["xp"],
        "gold_reward": base["gold"]
    }
    pass

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")
        
    pass

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is already dead and cannot fight.")

        display_battle_log("Battle started!")
        display_combat_stats(self.character, self.enemy)

        while self.combat_active:
            # Player turn
            winner = self.player_turn()
            if winner:
                return winner

            # Enemy turn
            winner = self.enemy_turn()
            if winner:
                return winner

        return {"winner": None, "xp_gained": 0, "gold_gained": 0}
        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError()

        display_battle_log("\n--- PLAYER TURN ---")

        print("Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run")

        # For testing we auto choose Basic Attack
        choice = "1"

        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You dealt {damage} damage!")
        elif choice == "2":
            msg = use_special_ability(self.character, self.enemy)
            display_battle_log(msg)
        elif choice == "3":
            if self.attempt_escape():
                return {"winner": "escaped", "xp_gained": 0, "gold_gained": 0}
            else:
                display_battle_log("You failed to escape!")

        return self.check_battle_end()
        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError()

        display_battle_log("\n--- ENEMY TURN ---")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} dealt {damage} damage!")

        return self.check_battle_end()
        pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        raw = attacker["strength"] - (defender["strength"] // 4)
        return max(1, raw)
        pass
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target["health"] = max(0, target["health"] - damage)
        pass
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy["health"] <= 0:
            display_battle_log("Enemy defeated!")
            rewards = get_victory_rewards(self.enemy)
            self.combat_active = False
            return {"winner": "player", **rewards}

        if self.character["health"] <= 0:
            display_battle_log("You were defeated!")
            self.combat_active = False
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

        return None
        pass
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        if random.random() < 0.5:
            display_battle_log("You escaped successfully!")
            self.combat_active = False
            return True
        return False
        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    role = character["class"].lower()

    if role == "warrior":
        return warrior_power_strike(character, enemy)
    elif role == "mage":
        return mage_fireball(character, enemy)
    elif role == "rogue":
        return rogue_critical_strike(character, enemy)
    elif role == "cleric":
        return cleric_heal(character)

    raise AbilityOnCooldownError("Ability not implemented or on cooldown.")
    pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - damage)
    return f"Warrior used Power Strike for {damage} damage!"
    
    pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - damage)
    return f"Mage used Fireball for {damage} damage!"
    pass

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        damage = character["strength"] * 3
        enemy["health"] = max(0, enemy["health"] - damage)
        return f"Rogue landed a CRITICAL STRIKE for {damage} damage!"
    else:
        return "Rogue attempted Critical Strike but missed!"
    pass

def cleric_heal(character):
    """Cleric special ability"""
    heal = 30
    character["health"] = min(character["max_health"], character["health"] + heal)
    return f"Cleric healed for {heal} HP!"

    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    return character["health"] > 0
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {"xp_gained": enemy["xp_reward"], "gold_gained": enemy["gold_reward"]}
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    try:
        goblin = create_enemy("goblin")
        print("Enemy Created:", goblin)
    except InvalidTargetError as e:
        print("Enemy creation failed:", e)

    # Test player data
    test_char = {
        "name": "Hero",
        "class": "Warrior",
        "health": 100,
        "max_health": 100,
        "strength": 15,
        "magic": 4
    }

    # Run a simple battle
    battle = SimpleBattle(test_char, goblin)
    result = battle.start_battle()
    print("\nBattle Result:", result)

