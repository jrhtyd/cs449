import tkinter as tk
from tkinter import ttk

class SolitaireGame:
    
    def __init__(self, start):
        self.start = start
        start.title("Solitaire")
        start.configure(bg='white')
        self.boardType = tk.StringVar()
        self.boardType.set('english')
        self.canvas = None
        self.cellPegs = []
        self.createUI()
        self.board()

    def createUI(self):
        header = ttk.Label(self.start, text="Solitaire")
        header.configure(font=('Times New Roman', 16))
        header.pack()
        
        mainFrame = ttk.Frame(self.start)
        mainFrame.pack(fill='both', expand=True)
        mainFrame.columnconfigure(0, weight=0)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.columnconfigure(2, weight=0)
        
        leftPanel = ttk.LabelFrame(mainFrame, text="Board Type")
        leftPanel.grid(row=1, column=0)
        
        boardTypes = []
        boardTypes.append(('english', 'English'))
        boardTypes.append(('hexagon', 'Hexagon'))
        boardTypes.append(('diamond', 'Diamond'))
        for value, text in boardTypes:
            button = ttk.Radiobutton(leftPanel, text=text, variable=self.boardType, value=value)
            button.configure(command=self.board)
            button.pack(anchor='w')
        
        self.boardFrame = ttk.Frame(mainFrame)
        self.boardFrame.grid(row=1, column=1)
        self.canvasFrame = tk.Frame(self.boardFrame)
        self.canvasFrame.pack(expand=True)
        
        rightPanel = ttk.Frame(mainFrame)
        rightPanel.grid(row=1, column=2)
        
        newGameButton = ttk.Button(rightPanel, text="New Game", width=12)
        newGameButton.configure(command=self.board)
        newGameButton.pack()
        
        ttk.Separator(rightPanel, orient='horizontal').pack(fill='x')
        
        autoplayButton = ttk.Button(rightPanel, text="Autoplay", width=12)
        autoplayButton.pack()
        randomizeButton = ttk.Button(rightPanel, text="Randomize", width=12)
        randomizeButton.pack()
        
        ttk.Separator(rightPanel, orient='horizontal').pack(fill='x')
        
        replayButton = ttk.Button(rightPanel, text="Replay", width=12)
        replayButton.pack()

    def getLayout(self):
        selected = self.boardType.get()
        if selected == 'english':
            return self.createEnglishBoard()
        elif selected == 'hexagon':
            return self.createEuropeanBoard()
        else:
            return self.createDiamondBoard()

    def createEnglishBoard(self):
        board = []
        
        row = 0
        while row < 7:
            currentRow = []
            column = 0
            while column < 7:
                isCorner = False
                if row < 2:
                    if column < 2:
                        isCorner = True
                    if column >= 5:
                        isCorner = True
                if row >= 5:
                    if column < 2:
                        isCorner = True
                    if column >= 5:
                        isCorner = True
                    
                if isCorner == True:
                    currentRow.append(0)
                elif row == 3 and column == 3:
                    currentRow.append(2)
                else:
                    currentRow.append(1)
                column = column + 1
            board.append(currentRow)
            row = row + 1
        return board

    def createEuropeanBoard(self):
        board = []
        
        row = 0
        while row < 7:
            currentRow = []
            column = 0
            while column < 7:
                rowDistance = 0
                columnDistance = 0
                
                if row < 2:
                    rowDistance = 2 - row
                elif row >= 5:
                    rowDistance = row - 4
                    
                if column < 2:
                    columnDistance = 2 - column
                elif column >= 5:
                    columnDistance = column - 4
                
                if rowDistance + columnDistance > 2:
                    currentRow.append(0)
                elif row == 3 and column == 3:
                    currentRow.append(2)
                else:
                    currentRow.append(1)
                column = column + 1
            board.append(currentRow)
            row = row + 1
        return board

    def createDiamondBoard(self):
        board = []
        
        row = 0
        while row < 9:
            currentRow = []
            column = 0
            while column < 9:
                distance = abs(row - 4) + abs(column - 4)
                
                if distance > 4:
                    currentRow.append(0)
                elif row == 4 and column == 4:
                    currentRow.append(2)
                else:
                    currentRow.append(1)
                column = column + 1
            board.append(currentRow)
            row = row + 1
        return board

    def board(self):
        children = self.canvasFrame.winfo_children()
        for child in children:
            child.destroy()
            
        board = self.getLayout()
        gridSize = len(board)
        cellSize = 20
        canvasSize = gridSize * cellSize + 10
        
        self.canvas = tk.Canvas(self.canvasFrame, width=canvasSize, height=canvasSize)
        self.canvas.configure(highlightthickness=0)
        self.canvas.pack()
        
        self.cellPegs = []
        
        row = 0
        while row < gridSize:
            pegRow = []
            column = 0
            while column < gridSize:
                x1 = column * cellSize + 1
                y1 = row * cellSize + 1
                x2 = x1 + cellSize
                y2 = y1 + cellSize
                centerX = (x1 + x2) // 2
                centerY = (y1 + y2) // 2
                radius = cellSize // 4
                
                self.canvas.create_rectangle(x1, y1, x2, y2, width=1)
                
                cellState = board[row][column]
                
                if cellState == 0:
                    pegRow.append(None)
                elif cellState == 1:
                    peg = self.canvas.create_oval(centerX - radius, centerY - radius, centerX + radius, centerY + radius)
                    self.canvas.itemconfig(peg, fill='black', outline='black', width=1)
                    pegRow.append(peg)
                else:
                    peg = self.canvas.create_oval(centerX - radius, centerY - radius, centerX + radius, centerY + radius)
                    self.canvas.itemconfig(peg, fill='white', outline='black', width=1)
                    pegRow.append(peg)
                column = column + 1
            self.cellPegs.append(pegRow)
            row = row + 1


def main():
    start = tk.Tk()
    start.geometry("600x500")
    
    game = SolitaireGame(start)
    start.mainloop()


if __name__ == "__main__":
    main()
