import tkinter as tk
from tkinter import ttk

class SolitaireLogic:
    def create_english_board(self, size=7):
        board = []
        arm = size // 3
        for row in range(size):
            current_row = []
            for col in range(size):
                is_corner = (row < arm or row >= size - arm) and (col < arm or col >= size - arm)
                if is_corner:
                    current_row.append(0)
                elif row == size // 2 and col == size // 2:
                    current_row.append(2)
                else:
                    current_row.append(1)
            board.append(current_row)
        return board

    def create_diamond_board(self, size=9):
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
        board = self.create_english_board(size)
        arm = size // 3
        if size >= 7:
            for r, c in [(arm-1, arm), (arm-1, size-arm-1), (size-arm, arm), (size-arm, size-arm-1)]:
                if 0 <= r < size and 0 <= c < size:
                    board[r][c] = 1
        return board

class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire")
        self.logic = SolitaireLogic()
        self.board_type = tk.StringVar(value='english')
        self.board_size = tk.StringVar(value="7")
        self.create_ui()
        self.refresh_board()

    def create_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side='top', fill='x', padx=10, pady=5)
        
        ttk.Label(top_frame, text="Board size").pack(side='right')
        size_entry = ttk.Entry(top_frame, textvariable=self.board_size, width=5)
        size_entry.pack(side='right', padx=5)
        size_entry.bind("<Return>", lambda e: self.refresh_board())

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        left_panel = ttk.LabelFrame(main_frame, text="Board Type")
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        for val, txt in [('english', 'English'), ('hexagon', 'Hexagon'), ('diamond', 'Diamond')]:
            ttk.Radiobutton(left_panel, text=txt, variable=self.board_type, value=val, command=self.refresh_board).pack(anchor='w')

        self.canvas_frame = tk.Frame(main_frame, bg='white')
        self.canvas_frame.grid(row=0, column=1, padx=20, pady=20)

        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=2, padx=10, pady=10, sticky='n')
        ttk.Button(right_panel, text="New Game", command=self.refresh_board).pack()

    def refresh_board(self):
        for child in self.canvas_frame.winfo_children():
            child.destroy()
        try:
            sz = int(self.board_size.get())
        except ValueError:
            sz = 7
        
        b_type = self.board_type.get()
        if b_type == 'english':
            data = self.logic.create_english_board(sz)
        elif b_type == 'diamond':
            data = self.logic.create_diamond_board(sz)
        else:
            data = self.logic.create_european_board(sz)
        self.draw_canvas(data, sz)

    def draw_canvas(self, board_data, size):
        cell_size = 35
        canvas = tk.Canvas(self.canvas_frame, width=size*cell_size, height=size*cell_size, bg='white', highlightthickness=0)
        canvas.pack()
        for r in range(size):
            for c in range(size):
                x1, y1 = c * cell_size, r * cell_size
                state = board_data[r][c]
                if state > 0:
                    canvas.create_rectangle(x1, y1, x1+cell_size, y1+cell_size, outline="black")
                    color = "black" if state == 1 else "white"
                    canvas.create_oval(x1+5, y1+5, x1+cell_size-5, y1+cell_size-5, fill=color, outline="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()
