import unittest
from game import new_game, apply_action


class TestGame(unittest.TestCase):

    def test_t1_new_game_start_state(self):
        """A new player should start with the correct state."""
        player = new_game("Jacob")

        self.assertEqual(player["name"], "Jacob")
        self.assertEqual(player["location"], "Beach")
        self.assertEqual(player["energy"], 5)
        self.assertEqual(player["inventory"], [])
        self.assertFalse(player["game_over"])
        self.assertIsNone(player["result"])

    def test_t2_invalid_command_changes_nothing(self):
        """An invalid command should not change the player's state."""
        player = new_game("Jacob")

        original_state = player.copy()
        original_state["inventory"] = player["inventory"].copy()

        apply_action(player, "fly")

        self.assertEqual(player, original_state)

    def test_t3_legal_move_costs_one_energy(self):
        """A successful movement should consume one energy point."""
        player = new_game("Jacob")
        starting_energy = player["energy"]

        apply_action(player, "east")

        self.assertEqual(player["location"], "Forest")
        self.assertEqual(player["energy"], starting_energy - 1)

    def test_t5_rusty_key_collected_once(self):
        """The Rusty Key should only be collected once."""
        player = new_game("Jacob")
        player["location"] = "Village"

        apply_action(player, "pickup")
        apply_action(player, "pickup")

        self.assertEqual(player["inventory"].count("Rusty Key"), 1)

    def test_t6_bridge_blocked_without_rusty_key(self):
        """The player cannot cross the bridge without the Rusty Key."""
        player = new_game("Jacob")
        player["location"] = "Jungle"

        starting_energy = player["energy"]

        apply_action(player, "east")

        self.assertEqual(player["location"], "Jungle")
        self.assertEqual(player["energy"], starting_energy)

    def test_t7_beacon_blocked_without_required_items(self):
        """The Beacon cannot be activated without Torch and Crystal."""
        player = new_game("Jacob")
        player["location"] = "Beacon"
        player["inventory"] = ["Rusty Key", "Torch"]

        apply_action(player, "light")

        self.assertFalse(player["game_over"])
        self.assertIsNone(player["result"])

    def test_t8_correct_inventory_wins(self):
        """The player wins when carrying Torch and Crystal at the Beacon."""
        player = new_game("Jacob")
        player["location"] = "Beacon"
        player["inventory"] = ["Rusty Key", "Torch", "Crystal"]

        apply_action(player, "light")

        self.assertTrue(player["game_over"])
        self.assertEqual(player["result"], "win")

    def test_t9_energy_exhaustion_loses(self):
        """The game should end when the player's energy reaches zero."""
        player = new_game("Jacob")
        player["location"] = "Beach"
        player["energy"] = 1

        apply_action(player, "east")

        self.assertEqual(player["location"], "Forest")
        self.assertEqual(player["energy"], 0)
        self.assertTrue(player["game_over"])
        self.assertEqual(player["result"], "lose")

    def test_t10_replay_resets_state(self):
        """Starting a new game should create a fresh player state."""
        first_game = new_game("Jacob")

        first_game["location"] = "Beacon"
        first_game["energy"] = 1
        first_game["inventory"].append("Rusty Key")

        second_game = new_game("Jacob")

        self.assertEqual(second_game["location"], "Beach")
        self.assertEqual(second_game["energy"], 5)
        self.assertEqual(second_game["inventory"], [])
        self.assertFalse(second_game["game_over"])
        self.assertIsNone(second_game["result"])

        # Ensure both games have independent inventory lists.
        self.assertIsNot(
            first_game["inventory"],
            second_game["inventory"]
        )


if __name__ == "__main__":
    unittest.main()