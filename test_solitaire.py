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

if __name__ == '__main__':
    unittest.main()
