from game import new_game, available_actions, apply_action, LOCATIONS


def play():
    """Run one complete game session."""

    print("\n" + "=" * 40)
    print("          MYSTERY ISLAND")
    print("=" * 40)

    print("\nWelcome to Mystery Island!")
    print("Your mission is to explore the mysterious island,")
    print("collect useful items, and light the Beacon.")
    print("Be careful! You have limited energy.")
    print("Type 'quit' whenever you want to leave.")

    name = input("\nYour name: ").strip()

    if not name:
        name = "Adventurer"

    player = new_game(name)

    while not player["game_over"]:

        current_location = player["location"]
        location_info = LOCATIONS[current_location]

        print("\n" + "-" * 40)
        print(f"Player: {player['name']}")
        print(f"Location: {current_location}")
        print(f"Energy: {player['energy']}")
        print(f"\n{location_info['description']}")

        actions = available_actions(player)

        print("\nAvailable actions:")

        for number, action in enumerate(actions, start=1):
            print(f"{number}. {action}")

        choice = input("\nChoose an action: ").strip().lower()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(actions):
                choice = actions[number - 1]
            else:
                print("Invalid number. Try again.")
                continue

        message = apply_action(player, choice)

        print(f"\n{message}")

    print("\n" + "=" * 40)
    print("             GAME OVER")
    print("=" * 40)

    if player["result"] == "win":
        print(f"Congratulations, {player['name']}! You escaped the mystery and won!")

    elif player["result"] == "lose":
        print(f"Sorry, {player['name']}. You ran out of energy!")

    elif player["result"] == "quit":
        print(f"Thanks for exploring Mystery Island, {player['name']}!")

    print(f"Final energy: {player['energy']}")
    print(f"Final inventory: {player['inventory']}")


def main():
    """Allow the player to replay the game."""

    while True:
        play()

        replay = input("\nWould you like to explore Mystery Island again? (yes/no): ")
        replay = replay.strip().lower()

        if replay not in ("yes", "y"):
            print("\nThanks for playing Mystery Island. Goodbye!")
            break


if __name__ == "__main__":
    main()