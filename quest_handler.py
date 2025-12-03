"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Kabijah Hill

AI Usage: help indention issues and debugging

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")

    quest = quest_data_dict[quest_id]

    # Check level requirement
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(
            f"Requires level {quest['required_level']}."
        )

    # Check prerequisite
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        raise QuestRequirementsNotMetError(
            f"Must complete prerequisite quest: {prereq}"
        )

    # Check already completed
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(
            f"Quest '{quest_id}' already completed."
        )

    # Check already active
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError(
            f"Quest '{quest_id}' already active."
        )

    # Accept quest
    character['active_quests'].append(quest_id)
    return True


    
    pass

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")

    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    quest = quest_data_dict[quest_id]

    # Remove from active, move to completed
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)

    # Grant rewards
    reward_xp = quest['reward_xp']
    reward_gold = quest['reward_gold']

    # Import here to avoid circular import at top
    from character_manager import gain_experience, add_gold

    gain_experience(character, reward_xp)
    add_gold(character, reward_gold)

    return {
        "reward_xp": reward_xp,
        "reward_gold": reward_gold
    }
    pass

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    """
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    character['active_quests'].remove(quest_id)
    return True
    pass

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    return [
        quest_data_dict[qid]
        for qid in character['active_quests']
        if qid in quest_data_dict
    ]

    pass

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    return [
        quest_data_dict[qid]
        for qid in character['completed_quests']
        if qid in quest_data_dict
    ]
    pass

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available = []

    for qid, quest in quest_data_dict.items():
        if qid in character['completed_quests']:
            continue
        if qid in character['active_quests']:
            continue
        if character['level'] < quest['required_level']:
            continue

        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in character['completed_quests']:
            continue

        available.append(quest)

    return available
    pass

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character['completed_quests']

    pass

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character['active_quests']
    pass

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    if character['level'] < quest['required_level']:
        return False

    if quest_id in character['completed_quests']:
        return False

    if quest_id in character['active_quests']:
        return False

    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False

    return True
    pass

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Invalid prerequisite: {current}")

        chain.insert(0, current)

        prereq = quest_data_dict[current]['prerequisite']
        if prereq == "NONE":
            break

        current = prereq

    return chain
    pass

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total = len(quest_data_dict)
    if total == 0:
        return 0.0

    completed = len(character['completed_quests'])
    return (completed / total) * 100
    pass

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0

    for qid in character['completed_quests']:
        if qid in quest_data_dict:
            total_xp += quest_data_dict[qid]['reward_xp']
            total_gold += quest_data_dict[qid]['reward_gold']

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }
    pass

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    return [
        quest
        for quest in quest_data_dict.values()
        if min_level <= quest['required_level'] <= max_level
    ]

    pass

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}")
    pass

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    for quest in quest_list:
        print(f"- {quest['title']} (Lvl {quest['required_level']}) "
              f"| XP: {quest['reward_xp']} | Gold: {quest['reward_gold']}")

    pass

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    active = len(character['active_quests'])
    completed = len(character['completed_quests'])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active Quests: {active}")
    print(f"Completed Quests: {completed}")
    print(f"Overall Completion: {percent:.2f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")

    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for qid, quest in quest_data_dict.items():
        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Quest '{qid}' has invalid prerequisite '{prereq}'."
            )
    return True
    pass


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

