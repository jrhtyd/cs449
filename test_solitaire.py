import unittest
from solitaire_logic import SolitaireLogic

class TestSolitaireLogic(unittest.TestCase):
    def setUp(self):
        """Initialize the logic class before each test."""
        self.logic = SolitaireLogic()

    def test_board_dimensions(self):
        """
        Feature: Choose board size and type[cite: 6, 21].
        AC 1.1: Verify the English board is initialized as a square grid 
        based on the input size.
        """
        size = 7
        layout = self.logic.create_english_board(size)
        self.assertEqual(len(layout), size, "Board height should match input size")
        self.assertEqual(len(layout[0]), size, "Board width should match input size")

    def test_initial_hole_position(self):
        """
        Feature: Start a new game[cite: 6, 21].
        AC 2.1: Verify the center cell (3,3) on a size 7 board 
        is an empty hole (represented by the integer 2).
        """
        size = 7
        layout = self.logic.create_english_board(size)
        # Center of a 7x7 board is index [3][3]
        center_cell = layout[3][3]
        self.assertEqual(center_cell, 2, "Center cell should be an empty hole (2)")

    def test_diamond_board_initialization(self):
        """
        Feature: Choose board size and type[cite: 21].
        Verify that the Diamond board layout scales correctly.
        """
        size = 9
        layout = self.logic.create_diamond_board(size)
        self.assertEqual(len(layout), size)
        # Verify the center of the diamond is the empty hole
        self.assertEqual(layout[4][4], 2)
import unittest
from gui import ManualGame, AutoGame

class TestSolitaire(unittest.TestCase):

    def setUp(self):
        # Testing with English board, size 7 (standard)
        self.manual_game = ManualGame('english', 7)
        self.auto_game = AutoGame('english', 7)

    ## --- Manual Game Tests ---
    def test_manual_initial_peg_count(self):
        # English 7x7 typically has 32 pegs and 1 empty center [cite: 7]
        self.assertEqual(self.manual_game.pegCount, 32)

    def test_manual_valid_selection(self):
        # Select a peg that has a valid move (e.g., above the center hole)
        # Center is (3,3), peg above is (1,3), jump over (2,3)
        can_select = self.manual_game.selectPeg(1, 3)
        self.assertTrue(can_select)
        self.assertEqual(self.manual_game.selectedPeg, (1, 3))

    def test_manual_move_execution(self):
        # Execute the move: (1,3) jump over (2,3) to (3,3)
        self.manual_game.selectPeg(1, 3)
        move_success = self.manual_game.tryMove(3, 3)
        self.assertTrue(move_success)
        self.assertEqual(self.manual_game.pegCount, 31)
        self.assertEqual(self.manual_game.board[1][3], 2) # Empty

    def test_randomize_state(self):
        # Ensure randomization changes the move count 
        initial_moves = self.manual_game.moveCount
        self.manual_game.randomize()
        self.assertEqual(self.manual_game.moveCount, initial_moves + 1)

    ## --- Automated Game Tests ---
    def test_auto_step_logic(self):
        # Ensure autoStep reduces peg count [cite: 7, 32]
        initial_pegs = self.auto_game.pegCount
        success = self.auto_game.autoStep()
        self.assertTrue(success)
        self.assertEqual(self.auto_game.pegCount, initial_pegs - 1)

    def test_game_over_detection(self):
        # A new game is not over
        self.assertFalse(self.manual_game.isGameOver())

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
