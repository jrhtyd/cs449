class SolitaireLogic:
    def __init__(self):
        self.board = []

    def get_layout(self, board_type):
        if board_type == 'english':
            return self.create_english_board()
        elif board_type == 'hexagon':
            return self.create_european_board()
        else:
            return self.create_diamond_board()

    def create_english_board(self):
        board = []
        for row in range(7):
            current_row = []
            for col in range(7):
                is_corner = (row < 2 or row >= 5) and (col < 2 or col >= 5)
                if is_corner:
                    current_row.append(0)
                elif row == 3 and col == 3:
                    current_row.append(2) # Empty hole
                else:
                    current_row.append(1) # Peg
            board.append(current_row)
        return board

    def create_european_board(self):
        board = []
        for row in range(7):
            current_row = []
            for col in range(7):
                row_dist = max(0, 2 - row) if row < 2 else max(0, row - 4)
                col_dist = max(0, 2 - col) if col < 2 else max(0, col - 4)
                if row_dist + col_dist > 2:
                    current_row.append(0)
                elif row == 3 and col == 3:
                    current_row.append(2)
                else:
                    current_row.append(1)
            board.append(current_row)
        return board

    def create_diamond_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                distance = abs(row - 4) + abs(col - 4)
                if distance > 4:
                    current_row.append(0)
                elif row == 4 and col == 4:
                    current_row.append(2)
                else:
                    current_row.append(1)
            board.append(current_row)
        return board

import tkinter as tk
from tkinter import ttk
from solitaire_logic import SolitaireLogic

class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire")
        self.logic = SolitaireLogic()
        self.board_type = tk.StringVar(value='english')
        self.create_ui()
        self.refresh_board()

    def create_ui(self):
        # Header [cite: 7]
        ttk.Label(self.root, text="Solitaire", font=('Times New Roman', 16)).pack()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Left Panel: Board Type [cite: 12, 13]
        left_panel = ttk.LabelFrame(main_frame, text="Board Type")
        left_panel.grid(row=0, column=0, padx=10, sticky='n')
        
        for val, txt in [('english', 'English'), ('hexagon', 'Hexagon'), ('diamond', 'Diamond')]:
            ttk.Radiobutton(left_panel, text=txt, variable=self.board_type, 
                            value=val, command=self.refresh_board).pack(anchor='w')
        
        # Center: Board Canvas [cite: 15]
        self.canvas_frame = tk.Frame(main_frame)
        self.canvas_frame.grid(row=0, column=1)
        
        # Right Panel: Controls [cite: 14]
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=2, padx=10, sticky='n')
        ttk.Button(right_panel, text="New Game", command=self.refresh_board).pack(pady=5)

    def refresh_board(self):
        for child in self.canvas_frame.winfo_children():
            child.destroy()
            
        board_data = self.logic.get_layout(self.board_type.get())
        size = len(board_data)
        cell_size = 30
        canvas = tk.Canvas(self.canvas_frame, width=size*cell_size, height=size*cell_size)
        canvas.pack()
        
        for r in range(size):
            for c in range(size):
                x1, y1 = c * cell_size, r * cell_size
                if board_data[r][c] > 0:
                    canvas.create_rectangle(x1, y1, x1+cell_size, y1+cell_size, outline="gray")
                    color = "black" if board_data[r][c] == 1 else "white"
                    canvas.create_oval(x1+5, y1+5, x1+cell_size-5, y1+cell_size-5, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
