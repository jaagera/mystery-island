Energy starts at 5. Each legal move costs 1. Pickups, inventory, and invalid input cost 0.
Map: Beach ↔ Jungle ↔ Cave ↔ Old Bridge ↔ Lighthouse (backward moves allowed, and they cost energy).
Rope in the Jungle, lantern in the Cave.
Bridge needs rope. Lighting the beacon needs lantern and Lighthouse location.
Loop flag game_over, outcome in result (None, "won", "lost", "quit").

## game.py
Function	Responsibility
new_game()	Creates the player's initial state
available_actions()	Determines what the player can do
can_cross_bridge()	Checks the Rusty Key requirement
can_light_beacon()	Checks the Torch and Crystal requirements
apply_action()	Validates actions and changes game state
main()	Handles user input and displays information



# Engineering Decisions – Text-Based Mystery_Island

## 1. Project Architecture

The project is divided into three main files:

```text
mystery_island/
├── game.py
├── main.py
├── test_game.py
└── decisions.md
```

- **game.py:** Contains game mechanics, player state, movement rules, inventory management, and win/loss conditions.
- **main.py:** Handles user interaction, menu display, input collection, and game replay.
- **test_game.py:** Contains automated tests for verifying game behaviour.
- **decisions.md:** Documents important engineering decisions and the reasons behind them.

## 2. Player State Management

The player is represented using a Python dictionary.

```python
player = {
    "name": name,
    "location": "Beach",
    "energy": 5,
    "inventory": [],
    "game_over": False,
    "result": None
}
```

**Decision:** A dictionary is used because it allows related player information to be stored and accessed using meaningful keys.

Each new game receives a fresh inventory list to prevent inventory data from being shared between different game sessions.

## 3. Separation of Concerns

The game logic and user interface are kept separate.

- `game.py` handles decisions and state changes.
- `main.py` handles user input and displays messages.

**Decision:** Game logic functions should not directly use `input()` or `print()`.

Instead, `apply_action()` returns a message string, which `main.py` displays.

**Reason:** This makes the game easier to test, maintain, and extend.

## 4. Available Actions

The `available_actions(player)` function dynamically determines which actions the player can perform.

Available actions include:

- Movement between connected locations.
- Picking up available items.
- Checking inventory.
- Quitting the game.
- Lighting the Beacon when the player reaches it.

**Decision:** Actions are determined by the player's current location and inventory rather than using one fixed menu throughout the game.

## 5. Game Rules and Conditions

The adventure uses the following mechanics:

- The player starts with 5 energy.
- Every successful movement consumes 1 energy.
- The Rusty Key is required to cross the bridge.
- The Torch is required to enter the Dark Cave (if that location is implemented).
- The Torch and Crystal are required to light the Beacon.
- Lighting the Beacon results in victory.
- Running out of energy results in defeat.
- The player can quit at any time.

## 6. Boolean Game State

The `game_over` variable controls when the game loop stops.

```python
while not player["game_over"]:
    # Continue the game
```

The three ending conditions are:

- Win: `game_over = True`, `result = "win"`.
- Lose: `game_over = True`, `result = "lose"`.
- Quit: `game_over = True`, `result = "quit"`.

**Decision:** A separate `result` variable is maintained to distinguish between the different ending conditions.

## 7. Input Validation

The game validates player actions before changing the game state.

Invalid actions return an error message without changing the player's location, energy, or inventory.

Numbered menu choices are converted into their corresponding action names.

```python
choice = actions[number - 1]
```

**Reason:** Python list indexing starts at zero, while menu numbering starts at one.

## 8. Inventory Management

Items are stored in a list.

```python
player["inventory"].append(item)
```

**Decision:** The `append()` method is used to add items without replacing previously collected items.

The game also checks whether an item is already owned before allowing another pickup.

## 9. Game Loop and Replay

The main game loop repeatedly displays the current location, energy, and available actions until the game ends.

After the game ends, the player is asked whether they want to play again.

**Decision:** Each replay calls `new_game()` to create a fresh player state instead of reusing the previous session.

## 10. Python Concepts Applied

The project demonstrates practical use of:

- Variables and data types.
- Dictionaries and lists.
- Functions and return values.
- Conditional statements (`if`, `elif`, `else`).
- `while` and `for` loops.
- Boolean logic.
- String methods and f-strings.
- User input and type conversion.
- List indexing and `enumerate()`.
- Modules and imports.
- State management.
- Input validation.
- Automated testing.

## 11. Testing Strategy

The following scenarios should be tested:

1. A new player starts with 5 energy.
2. Two new games have independent inventory lists.
3. An item cannot be collected twice.
4. Invalid actions do not change player state.
5. Movement consumes exactly 1 energy.
6. The bridge cannot be crossed without the Rusty Key.
7. The Beacon cannot be lit without the required items.
8. Successful Beacon activation produces a win.
9. Running out of energy produces a loss.
10. Quitting produces a quit result.
11. A replay starts with a fresh player state.

## 12. Engineering Principle

The main engineering principle behind this project is **separation of concerns, predictable state management, and validation before state mutation.**

The goal is to build a program that is easy to understand, test, maintain, and extend without mixing user interaction with game logic.


## File summaries

### game.py: the rules (no player-facing input)
Holds all game logic and state.
- LOCATIONS: a dictionary mapping each place to its description, an optional
  item, and its exits (direction -> destination). One dictionary instead of
  separate variables per place, so the map is data and can change without
  touching the logic.
- new_game(name): returns a fresh player dictionary (name, location, energy 5,
  inventory, game_over, result). The inventory list is created inside the
  function so every replay gets a new list.
- available_actions(player): builds the list of valid actions from the current
  location, whether an unowned item is here, and the always-present
  inventory/quit.
- can_cross_bridge(player) / can_light_beacon(player): return True/False only.
  No printing, no state change, so they are easy to test.
- apply_action(player, action): the single entry point for every action. It
  cleans the input, handles quit, inventory, pickup, light and movement, and
  returns a message string. Invalid actions return a message and change
  nothing. Energy is subtracted only after the gate checks pass, and reaching 0
  sets game_over and result = "lose".
- Known issue: game.py still contains a main() with print/input. It
  duplicates main.py and will be removed.

### main.py: the interface (input and output only)
- play(): runs one game. Prints the title and instructions, asks for a name,
  then loops `while not player["game_over"]`: show status and numbered
  actions, read input, .strip().lower() it, convert a number to its action,
  call apply_action, print the message. After the loop it prints the outcome
  based on player["result"].
- main(): calls play() and asks about replaying. Each replay calls new_game
  again, so state is fresh.
- Contains no game rules. It only displays and passes input along.

### tests/test_game.py: the safety net
unittest tests that call game.py functions directly, with no typing needed.
- T1 start state, T2 invalid command changes nothing, T3 move costs 1 energy,
  T5 item collected once, T6 bridge blocked without the key, T7 beacon blocked
  without items, T8 correct inventory wins, T9 energy exhaustion loses,
  T10 replay resets state.
- Run with: python3 -m unittest discover -s tests -v
- Missing: T4 (wrong direction rejected at no cost) and a full winning-path
  test.

## Status at time of writing
- All 9 tests pass, but the game is not winnable: collecting all items and
  reaching the end takes 6 moves and energy is 5. The tests check rules in
  isolation, so they did not catch it.
- Fix in progress: shorten the map to Beach, Jungle, Cave, Old Bridge,
  Lighthouse (4 moves), add a winning-path test, remove main() from game.py.