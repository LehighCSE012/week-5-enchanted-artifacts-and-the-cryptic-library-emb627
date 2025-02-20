'''
Week 5 Coding Assignment: The Enchanted Artifacts and the Cryptic Library
'''

import random

def display_player_status(player_stats):
    """Displays the player's current health"""
    print(f"Your current health: {player_stats["health"]}")

def handle_path_choice(player_stats):
    """Randomly chooses the left or right path and applies the corresponding health effects"""
    path_choice = random.choice(["left", "right"])
    if path_choice == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats["health"] = player_stats["health"] + 10
        player_stats["health"] = min(player_stats["health"], 100)
    elif path_choice == "right":
        print("You fall into a pit and lose 15 health points.")
        player_stats["health"] = player_stats["health"] - 15
        if player_stats["health"] < 0:
            player_stats["health"] = 0
            print("You are barely alive!")
    return player_stats

def player_attack(player_stats, monster_health):
    """Changes the monster's health after the player attacks it"""
    monster_health = monster_health - player_stats["attack"]
    print(f"You strike the monster for {player_stats["attack"]} damage!")
    return monster_health

def monster_attack(player_stats):
    """Changes the player's health based on whether the monster lands a critical hit or not"""
    critical_hit = random.random()
    if critical_hit < 0.5:
        player_stats["health"] = player_stats["health"] - 20
        print("The monster lands a critical hit for 20 damage!")
    else:
        player_stats["health"] = player_stats["health"] - 10
        print("The monster hits you for 10 damage!")
    return player_stats

def acquire_item(inventory, item):
    """Allows for items to be added to the inventory, whether single items or lists of items"""
    if not item:
        print("You found nothing.")
    else:
        inventory.append(item) #Operation 1: "Append" used to add single item to inventory
        print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """Shows the player what is in their inventory or if it is empty"""
    if inventory == [ ]:
        print("Your inventory is empty.")
    else:
        print("Your inventory:") #Prints header once
        for index, item in enumerate(inventory):
            print(f"{index + 1}. {item}") #Prints numbered list of each item on a newline

def use_item(inventory):
    """Allows player to try and fail to use the spell book, then discards it from the inventory"""
    if "spell book" in inventory: #Operation 2:"In" checks if spell book is within the inventory
        inventory.remove("spell book") #Operation 3: "Remove" discards spell book from inventory
        print("You opened the spell book but could not read its language, so you discarded it.")
    return inventory

def find_clue(clues, new_clue):
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        #Set method 1: add() allows me to add the new_clue into the clues set
        print(f"You discovered a new clue: {new_clue}.")
    return clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """Allows player to find an artifact, use its effect, then remove it from the dictionary"""
    if artifact_name in artifacts:
        if artifacts[artifact_name].get("discovered", False):
            #Dict method 1: get() allows me to access the discovered key if it exists but
            #won't give me a KeyError if it doesn't
            print("You've alerady discovered this item.")
        else:
            print(f"You discovered {artifacts[artifact_name]["description"]}.")
            if artifacts[artifact_name]["effect"] == "increases health":
                player_stats["health"] = player_stats["health"] + artifacts[artifact_name]["power"]
                print(f"This artifact {artifacts[artifact_name]["effect"]}.")
            elif artifacts[artifact_name]["effect"] == "enhances attack":
                player_stats["attack"] = player_stats["attack"] + artifacts[artifact_name]["power"]
                print(f"This artifact {artifacts[artifact_name]["effect"]}.")
            elif artifacts[artifact_name]["effect"] == "solves puzzles":
                print(f"This artifact {artifacts[artifact_name]["effect"]}.")
            artifacts[artifact_name].update({"discovered": True})
            #Dict method 2: update() allows me to add a new key-value pair to the artifact dict,
            #so that I can track which artifacts were already discovered
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def combat_encounter(player_stats, monster_health, has_treasure):
    """Describes combat encounters: player and then monster take turns attacking
    each other and health values update, a win or loss is determined at the end"""
    if monster_health <= 0:
        return False
    while player_stats["health"] > 0 and monster_health > 0:
        #Player's turn
        monster_health = player_attack(player_stats, monster_health)
        display_player_status(player_stats["health"])

        #Monster's turn
        monster_attack(player_stats)

    #Win/Loss check
    if player_stats["health"] <= 0:
        print("Game Over!")
        return False
    if monster_health <= 0:
        print("You defeated the monster!")
        if has_treasure:
            return True
        else:
            return False

def check_for_treasure(has_treasure):
    """Checking if the monster had treasure"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, bypass_ability):
    """Takes player through each of the dungeon rooms"""
    for room in dungeon_rooms:
        print(f"You enter {room[0]}!")
        if room[1] is not None:
            print(f"You found a {room[1]} in the room.")
            acquire_item(inventory, room[1])

        if room[2] == "trap": #Path if the player enters the lava trap room
            print("You see a potential trap!")
            trap_choice = input("Disarm or bypass the trap?")
            if trap_choice == "disarm": #If the player attempts to disarm the trap
                success = random.choice([True, False])
                if success:
                    print(f"{room[3][0]}")
                    player_stats["health"] = player_stats["health"] + room[3][2]
                    if player_stats["health"] <= 0:
                        print("Oh no, you have died!")
                        break
                else:
                    print(f"{room[3][1]}")
                    player_stats["health"] = player_stats["health"] + room[3][2]
                    if player_stats["health"] <= 0:
                        print("Oh no, you have died!")
                        break
            else: #If the player chooses to bypass the trap
                success = random.choice([True, False, False])
                if success:
                    print("You gained nothing, move on.")
                else:
                    print(f"{room[3][1]}")
                    player_stats["health"] = player_stats["health"] + room[3][2]
                    if player_stats["health"] <= 0:
                        print("Oh no, you have died!")
                        break
                display_inventory(inventory)

        elif room[2] == "puzzle": #Path if the player enters the chest puzzle room
            print("You encounter a puzzle!")
            if bypass_ability:
                bypass = input("Do you want to use the staff of wisdom?")
                if bypass == "yes":
                    print("You have used your knowledge to bypass this puzzle.")
                    player_stats["health"] = player_stats["health"] + room[3][2]
                    bypass_ability = False

            else:
                puzzle_choice = input("Solve or skip?")
                if puzzle_choice == "solve": 
                    success = random.choice([True, False])
                    if success: #Path if the player solves the puzzle
                        print(f"{room[3][0]}")
                        player_stats["health"] = player_stats["health"] + room[3][2]
                        if player_stats["health"] <= 0:
                            print("Oh no, you have died!")
                            break
                    else: #Path if player fails to solve puzzle
                        print(f"{room[3][1]}")
                        player_stats["health"] = player_stats["health"] + room[3][2]
                        if player_stats["health"] <= 0:
                            print("Oh no, you have died!")
                            break
                else: #If the player chooses to skip the puzzle
                    success = random.choice([True, False, False])
                    if success:
                        print("You gained nothing, move on.")
                    else:
                        print(f"{room[3][1]}")
                        player_stats["health"] = player_stats["health"] + room[3][2]
                        if player_stats["health"] <= 0:
                            print("Oh no, you have died!")
                            break
            display_inventory(inventory)

        elif room[2] == "library": #Path if the player enters the library
            clue_list = [
                "Look behind the potraits.",
                "Maybe the monster knows more than you think.",
                "See past the gold.",
                "Where there are plants, there must be water."]
            selected_clues = random.sample(clue_list, 2)
            print(selected_clues)
            for clue in selected_clues:
                new_clue = clue
                clues = find_clue(clues, new_clue)
            if "staff_of_wisdom" in inventory:
                print("You understand the meaning of the clues and can now bypass a puzzle challenge in another room.")
                bypass_ability = True
        else: #Path if the player enters the maze with no challenge
            print("There doesn't seem to be a challenge in this room. You move on.")
            display_inventory(inventory)
    display_player_status(player_stats)
    return player_stats, inventory, bypass_ability

def main():
    """Main game logic with initialized variables"""
    dungeon_rooms = [("A room filled with lava", None, "trap",
                      ("You avoided the lava!", "You fell into the lava!", -10)),
                     ("A hedge maze", "spell book", None, None),
                     ("A dark room with portraits and locked chest", "pile of gold coins", "puzzle",
                      ("You unlocked the chest!", "The chest remains locked.", -5)),
                      ("A vast library filled with ancient, cryptic texts.", None, "library", None)]
    
    artifacts = {
        "magic_potion": {
            "description": "a blue potion that heals your injuries when drank.",
            "power": 15,
            "effect": "increases health"
        },
        "suit_of_armor": {
            "description": "a suit made of steel that protects you in combat.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "a tall, wooden staff that holds ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    #Initialized variables
    clues = set()
    player_stats = {"health": 100, "attack": 5}
    has_treasure = False
    monster_health = 60
    inventory = [ ]
    bypass_ability = False

    #Demonstrating tuple immutability: The following line will cause a TypeError
    #because tuples cannot be modified after they are created
    dungeon_rooms[1][1] = "magic potion"

    has_treasure = random.choice([True, False]) # Randomly assigns treasure

    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)

    treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)

    check_for_treasure(treasure_obtained_in_combat) # Or has_treasure, depending on logic

    if random.random() < 0.3:
        artifact_keys = list(artifacts.keys())
        #Dict method 3: keys() creates a list of all the keys in the artifacts dictionary, in this case,
        #it creates a list of artifact_names so that one can by randomly discovered
        if artifact_keys:
            artifact_name = random.choice(artifact_keys)
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)
    
    if player_stats["health"] > 0:
        player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues, bypass_ability)
        print("\n ---Game End---")
        display_player_status(player_stats)
        print("Final inventory:")
        display_inventory(inventory)
        print("Clues:")
        if clues:
            for clue in clues:
                #Set method 2: the "in" operator allows me to iterate through each clue in the clues set and print it
                print(f"-{clue}")
        else:
            print("No clues.")

if __name__ == "__main__":
    main()
