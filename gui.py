import tkinter as tk
from tkinter import ttk

# --- GAME LOGIC CLASS ---
class SolitaireLogic:
    """
    Handles the game rules, board generation, and state validation.
    Separated from the GUI class to follow MVC principles.
    """
    def create_english_board(self, size=7):
        """Generates an English cross-shaped board."""
        board = []
        arm = size // 3
        for row in range(size):
            current_row = []
            for col in range(size):
                is_corner = (row < arm or row >= size - arm) and \
                            (col < arm or col >= size - arm)
                if is_corner:
                    current_row.append(0)  # Invalid
                elif row == size // 2 and col == size // 2:
                    current_row.append(2)  # Initial empty hole
                else:
                    current_row.append(1)  # Peg
            board.append(current_row)
        return board

    def create_diamond_board(self, size=9):
        """Generates a Diamond-shaped board."""
        board = []
        center = size // 2
        for row in range(size):
            current_row = []
            for col in range(size):
                distance = abs(row - center) + abs(col - center)
                if distance > center:
                    current_row.append(0)
                elif row == center and col == center:
                    current_row.append(2)
                else:
                    current_row.append(1)
            board.append(current_row)
        return board

    def create_european_board(self, size=7):
        """Generates a European/Hexagon board."""
        board = self.create_english_board(size)
        arm = size // 3
        if size >= 7:
            for r, c in [(arm-1, arm), (arm-1, size-arm-1), 
                         (size-arm, arm), (size-arm, size-arm-1)]:
                if 0 <= r < size and 0 <= c < size:
                    board[r][c] = 1
        return board

# --- USER INTERFACE CLASS ---
class SolitaireGUI:
    """Handles the GUI layout and user interactions."""
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire")
        self.logic = SolitaireLogic()  # Dependency Injection
        self.board_type = tk.StringVar(value='english')
        self.board_size = tk.StringVar(value="7")
        self.create_ui()
        self.refresh_board()

    def create_ui(self):
        """Builds the GUI structure based on requirements."""
        # Header and Top Panel for Board Size
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side='top', fill='x', padx=10, pady=5)
        
        ttk.Label(top_frame, text="Board size").pack(side='right')
        size_entry = ttk.Entry(top_frame, textvariable=self.board_size, width=5)
        size_entry.pack(side='right', padx=5)
        size_entry.bind("<Return>", lambda e: self.refresh_board())

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Left: Board Type
        left_panel = ttk.LabelFrame(main_frame, text="Board Type")
        left_panel.grid(row=0, column=0, padx=10, sticky='n')
        for val, txt in [('english', 'English'), ('hexagon', 'Hexagon'), ('diamond', 'Diamond')]:
            ttk.Radiobutton(left_panel, text=txt, variable=self.board_type, 
                            value=val, command=self.refresh_board).pack(anchor='w')

        # Center: Game Canvas
        self.canvas_frame = tk.Frame(main_frame)
        self.canvas_frame.grid(row=0, column=1)

        # Right: New Game
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=2, padx=10,
