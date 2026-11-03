LOCATIONS = {
    "Beach": {
        "description": "You are standing on a quiet beach. A mysterious forest lies to the east.",
        "exits": {"east": "Forest"}
    },
    "Forest": {
        "description": "You are in a thick forest. You notice a torch on the ground.",
        "item": "Torch",
        "exits": {
            "west": "Beach",
            "north": "Village",
            "east": "Jungle"
        }
    },
    "Village": {
        "description": "You have discovered an abandoned village. A rusty key lies nearby.",
        "item": "Rusty Key",
        "exits": {
            "south": "Forest",
            "east": "Ruins"
        }
    },
    "Ruins": {
        "description": "You discover ancient ruins containing a mysterious crystal.",
        "item": "Crystal",
        "exits": {
            "west": "Village",
            "south": "Jungle"
        }
    },
    "Jungle": {
        "description": "A dangerous jungle surrounds you. An old bridge stands to the east.",
        "exits": {
            "west": "Forest",
            "north": "Ruins",
            "east": "Bridge"
        }
    },
    "Bridge": {
        "description": "You are standing on an ancient bridge leading to the mysterious Beacon.",
        "exits": {
            "west": "Jungle",
            "east": "Beacon"
        }
    },
    "Beacon": {
        "description": "You have reached the ancient Beacon! Its light could reveal the island's greatest secret.",
        "exits": {"west": "Bridge"}
    }
}


def new_game(name):
    """Create a fresh Mystery Island game session."""
    return {
        "name": name,
        "location": "Beach",
        "energy": 5,
        "inventory": [],
        "game_over": False,
        "result": None
    }


def available_actions(player):
    """Return the available actions based on the player's current state."""

    if player["game_over"]:
        return []

    actions = list(LOCATIONS[player["location"]]["exits"].keys())

    current_location = LOCATIONS[player["location"]]

    if "item" in current_location:
        item = current_location["item"]

        if item not in player["inventory"]:
            actions.append("pickup")

    actions.append("inventory")
    actions.append("quit")

    if player["location"] == "Beacon":
        actions.append("light")

    return actions


def can_cross_bridge(player):
    """Check whether the player has the Rusty Key."""
    return "Rusty Key" in player["inventory"]


def can_light_beacon(player):
    """Check whether the player has the required items to light the Beacon."""
    return (
        "Torch" in player["inventory"]
        and "Crystal" in player["inventory"]
    )


def apply_action(player, action):
    """Apply a player's action and return a descriptive message."""

    if player["game_over"]:
        return "Mystery Island is already finished."

    action = action.strip().lower()

    # Quit the game
    if action == "quit":
        player["game_over"] = True
        player["result"] = "quit"
        return "You have left Mystery Island."

    # Display inventory
    if action == "inventory":
        if player["inventory"]:
            return f"Your inventory: {', '.join(player['inventory'])}"

        return "Your inventory is empty."

    # Collect an item
    if action == "pickup":
        location = LOCATIONS[player["location"]]

        if "item" not in location:
            return "There is nothing to collect here."

        item = location["item"]

        if item in player["inventory"]:
            return "You already collected this item."

        player["inventory"].append(item)

        return f"You collected the {item}!"

    # Activate the Beacon
    if action == "light":
        if player["location"] != "Beacon":
            return "There is no Beacon here."

        if not can_light_beacon(player):
            return "You need a Torch and a Crystal to activate the Beacon."

        player["game_over"] = True
        player["result"] = "win"

        return (
            "Congratulations! You activated the ancient Beacon "
            "and uncovered the mystery of the island. You win!"
        )

    # Movement
    exits = LOCATIONS[player["location"]]["exits"]

    if action not in exits:
        return "Invalid action. Choose an available action."

    destination = exits[action]

    # Check bridge restrictions
    crossing_bridge = (
        (player["location"] == "Jungle" and destination == "Bridge")
        or
        (player["location"] == "Bridge" and destination == "Beacon")
    )

    if crossing_bridge and not can_cross_bridge(player):
        return "The bridge is locked! You need the Rusty Key."

    # Consume energy and move
    player["energy"] -= 1
    player["location"] = destination

    # Check energy exhaustion
    if player["energy"] <= 0:
        player["energy"] = 0
        player["game_over"] = True
        player["result"] = "lose"

        return (
            f"You reached {destination}, but ran out of energy. "
            "Your Mystery Island journey has ended!"
        )

    return (
        f"You moved to {destination}. "
        f"Energy remaining: {player['energy']}"
    )


def main():
    """Run Mystery Island from the terminal."""

    name = input("Enter your player name: ").strip()

    if not name:
        name = "Explorer"

    player = new_game(name)

    print("\n" + "=" * 40)
    print("          MYSTERY ISLAND")
    print("=" * 40)

    print(f"\nWelcome, {player['name']}!")
    print("Your mission is to explore the island.")
    print("Collect the required items and activate the ancient Beacon.")
    print("Be careful! Your energy is limited.")

    while not player["game_over"]:

        location = LOCATIONS[player["location"]]

        print("\n" + "=" * 40)
        print(f"Player: {player['name']}")
        print(f"Location: {player['location']}")
        print(location["description"])
        print(f"Energy: {player['energy']}")

        actions = available_actions(player)

        print("\nAvailable actions:")
        print(", ".join(actions))

        action = input("\nWhat would you like to do? ")

        message = apply_action(player, action)

        print("\n" + message)

    print("\n" + "=" * 40)
    print("          MYSTERY ISLAND")
    print("             GAME OVER")
    print("=" * 40)

    print(f"Player: {player['name']}")
    print(f"Result: {player['result']}")
    print(f"Final energy: {player['energy']}")
    print(f"Inventory: {player['inventory']}")


if __name__ == "__main__":
    main()