import tkinter as tk
import random


class BoardGame:
    def __init__(self, boardType, boardSize):
        self.boardType = boardType
        self.boardSize = boardSize
        self.board = []
        self.moveHistory = []
        self.pegCount = 0
        self.moveCount = 0
        self.setupBoard()

    def setupBoard(self):
        self.board = []
        self.moveHistory = []
        self.moveCount = 0
        self.pegCount = 0

        bType = self.boardType.strip().lower()
        if bType == 'english':
            self.board = self.makeEnglish()
        elif bType == 'hexagon':
            self.board = self.makeEuropean()
        elif bType == 'diamond':
            self.board = self.makeDiamond()
        else:
            self.board = self.makeEnglish()

        r = 0
        while r < len(self.board):
            c = 0
            while c < len(self.board[r]):
                if self.board[r][c] == 1:
                    self.pegCount = self.pegCount + 1
                c = c + 1
            r = r + 1

    def makeEnglish(self):
        board = []
        arm = self.boardSize // 3
        r = 0
        while r < self.boardSize:
            row = []
            c = 0
            while c < self.boardSize:
                isCorner = (r < arm or r >= self.boardSize - arm) and (c < arm or c >= self.boardSize - arm)
                if isCorner:
                    row.append(0)
                elif r == self.boardSize // 2 and c == self.boardSize // 2:
                    row.append(2)
                else:
                    row.append(1)
                c = c + 1
            board.append(row)
            r = r + 1
        return board

    def makeEuropean(self):
        board = self.makeEnglish()
        arm = self.boardSize // 3
        if self.boardSize >= 7:
            spots = [(arm - 1, arm), (arm - 1, self.boardSize - arm - 1),
                     (self.boardSize - arm, arm), (self.boardSize - arm, self.boardSize - arm - 1)]
            i = 0
            while i < len(spots):
                r = spots[i][0]
                c = spots[i][1]
                if 0 <= r < self.boardSize and 0 <= c < self.boardSize:
                    board[r][c] = 1
                i = i + 1
        return board

    def makeDiamond(self):
        board = []
        center = self.boardSize // 2
        r = 0
        while r < self.boardSize:
            row = []
            c = 0
            while c < self.boardSize:
                dist = abs(r - center) + abs(c - center)
                if dist > center:
                    row.append(0)
                elif r == center and c == center:
                    row.append(2)
                else:
                    row.append(1)
                c = c + 1
            board.append(row)
            r = r + 1
        return board

    def getValidMoves(self, row, col):
        moves = []
        if self.board[row][col] != 1:
            return moves
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        i = 0
        while i < 4:
            dr = directions[i][0]
            dc = directions[i][1]
            midR = row + dr // 2
            midC = col + dc // 2
            endR = row + dr
            endC = col + dc
            if 0 <= endR < self.boardSize and 0 <= endC < self.boardSize:
                if self.board[midR][midC] == 1 and self.board[endR][endC] == 2:
                    moves.append((endR, endC, midR, midC))
            i = i + 1
        return moves

    def getAllMoves(self):
        allMoves = []
        r = 0
        while r < self.boardSize:
            c = 0
            while c < self.boardSize:
                if self.board[r][c] == 1:
                    moves = self.getValidMoves(r, c)
                    j = 0
                    while j < len(moves):
                        allMoves.append((r, c, moves[j]))
                        j = j + 1
                c = c + 1
            r = r + 1
        return allMoves

    def makeMove(self, fromR, fromC, toR, toC, midR, midC):
        self.moveHistory.append((fromR, fromC, toR, toC, midR, midC))
        self.board[fromR][fromC] = 2
        self.board[midR][midC] = 2
        self.board[toR][toC] = 1
        self.pegCount = self.pegCount - 1
        self.moveCount = self.moveCount + 1

    def undoMove(self):
        if len(self.moveHistory) == 0:
            return False
        last = self.moveHistory.pop()
        fromR = last[0]
        fromC = last[1]
        toR = last[2]
        toC = last[3]
        midR = last[4]
        midC = last[5]
        self.board[fromR][fromC] = 1
        self.board[midR][midC] = 1
        self.board[toR][toC] = 2
        self.pegCount = self.pegCount + 1
        self.moveCount = self.moveCount - 1
        return True

    def isGameOver(self):
        return len(self.getAllMoves()) == 0

    def hasWon(self):
        return self.pegCount == 1


class ManualGame(BoardGame):
    def __init__(self, boardType, boardSize):
        BoardGame.__init__(self, boardType, boardSize)
        self.selectedPeg = None
        self.validMoves = []

    def selectPeg(self, row, col):
        if self.board[row][col] != 1:
            self.selectedPeg = None
            self.validMoves = []
            return False
        self.selectedPeg = (row, col)
        self.validMoves = self.getValidMoves(row, col)
        return len(self.validMoves) > 0

    def tryMove(self, row, col):
        if self.selectedPeg is None:
            return False
        i = 0
        while i < len(self.validMoves):
            m = self.validMoves[i]
            if m[0] == row and m[1] == col:
                self.makeMove(self.selectedPeg[0], self.selectedPeg[1], m[0], m[1], m[2], m[3])
                self.selectedPeg = None
                self.validMoves = []
                return True
            i = i + 1
        return False

    def randomize(self):
        allMoves = self.getAllMoves()
        if len(allMoves) == 0:
            return False
        pick = random.randint(0, len(allMoves) - 1)
        fromR, fromC, moveData = allMoves[pick]
        self.makeMove(fromR, fromC, moveData[0], moveData[1], moveData[2], moveData[3])
        self.selectedPeg = None
        self.validMoves = []
        return True


class AutoGame(BoardGame):
    def __init__(self, boardType, boardSize):
        BoardGame.__init__(self, boardType, boardSize)

    def autoStep(self):
        allMoves = self.getAllMoves()
        if len(allMoves) == 0:
            return False
        bestMove = None
        bestScore = -1
        i = 0
        while i < len(allMoves):
            fromR, fromC, moveData = allMoves[i]
            toR = moveData[0]
            toC = moveData[1]
            score = 0
            centerR = self.boardSize // 2
            centerC = self.boardSize // 2
            distBefore = abs(fromR - centerR) + abs(fromC - centerC)
            distAfter = abs(toR - centerR) + abs(toC - centerC)
            if distAfter < distBefore:
                score = score + 2
            if bestMove is None or score > bestScore:
                bestScore = score
                bestMove = allMoves[i]
            i = i + 1
        if bestMove is not None:
            fromR, fromC, moveData = bestMove
            self.makeMove(fromR, fromC, moveData[0], moveData[1], moveData[2], moveData[3])
            return True
        return False


class SolitaireGame:
    def __init__(self, start):
        self.start = start
        self.start.title("Solitaire")
        self.start.geometry("600x500")

        self.boardType = tk.StringVar()
        self.boardType.set('english')
        self.boardSize = tk.StringVar()
        self.boardSize.set('7')
        self.gameMode = tk.StringVar()
        self.gameMode.set('manual')
        self.recordVar = tk.IntVar()
        self.recordVar.set(0)

        self.game = None
        self.cellPegs = []
        self.autoRunning = False
        self.replayRunning = False
        self.replayMoves = []
        self.replayIndex = 0
        self.replayBoardType = ''
        self.replayBoardSize = 0
        self.replayMode = ''
        self.recordFile = 'game_record.txt'

        self.buildLayout()
        self.newGame()

    def buildLayout(self):
        self.leftFrame = tk.Frame(self.start)
        self.leftFrame.pack(side='left', fill='y')

        self.canvasFrame = tk.Frame(self.start)
        self.canvasFrame.pack(side='left', expand=True)

        self.rightFrame = tk.Frame(self.start)
        self.rightFrame.pack(side='right', fill='y')

        tk.Label(self.leftFrame, text="Board Type").pack()
        tk.Radiobutton(self.leftFrame, text="English", variable=self.boardType, value='english').pack(anchor='w')
        tk.Radiobutton(self.leftFrame, text="Hexagon", variable=self.boardType, value='hexagon').pack(anchor='w')
        tk.Radiobutton(self.leftFrame, text="Diamond", variable=self.boardType, value='diamond').pack(anchor='w')

        tk.Label(self.leftFrame, text="").pack()
        tk.Label(self.leftFrame, text="Game Mode").pack()
        tk.Radiobutton(self.leftFrame, text="Manual", variable=self.gameMode, value='manual').pack(anchor='w')
        tk.Radiobutton(self.leftFrame, text="Automated", variable=self.gameMode, value='automated').pack(anchor='w')

        tk.Label(self.leftFrame, text="").pack()
        tk.Checkbutton(self.leftFrame, text="Record game", variable=self.recordVar).pack(anchor='w')

        tk.Label(self.rightFrame, text="Board size").pack()
        tk.Entry(self.rightFrame, textvariable=self.boardSize, width=3).pack()

        tk.Label(self.rightFrame, text="").pack()
        tk.Button(self.rightFrame, text="Replay", command=self.replay).pack()
        tk.Button(self.rightFrame, text="New Game", command=self.newGame).pack()
        tk.Button(self.rightFrame, text="Autoplay", command=self.autoplay).pack()
        tk.Button(self.rightFrame, text="Randomize", command=self.randomize).pack()
        tk.Button(self.rightFrame, text="Undo", command=self.undo).pack()

        self.statusLabel = tk.Label(self.start, text="")
        self.statusLabel.pack(side='bottom')

    def newGame(self):
        self.autoRunning = False
        self.replayRunning = False
        try:
            size = int(self.boardSize.get())
        except:
            size = 7
        if size < 5:
            size = 5
        if size > 11:
            size = 11
        if size % 2 == 0:
            size = size + 1

        bType = self.boardType.get()
        mode = self.gameMode.get()

        if mode == 'manual':
            self.game = ManualGame(bType, size)
        else:
            self.game = AutoGame(bType, size)

        if self.recordVar.get() == 1:
            f = open(self.recordFile, 'w')
            f.write(bType + ' ' + str(size) + ' ' + mode + '\n')
            f.close()

        self.drawBoard()
        self.updateStatus()

    def writeMove(self, fromR, fromC, toR, toC, midR, midC):
        if self.recordVar.get() == 1:
            f = open(self.recordFile, 'a')
            f.write(str(fromR) + ' ' + str(fromC) + ' ' + str(toR) + ' ' + str(toC) + ' ' + str(midR) + ' ' + str(midC) + '\n')
            f.close()

    def replay(self):
        try:
            f = open(self.recordFile, 'r')
            lines = f.readlines()
            f.close()
        except:
            self.statusLabel.config(text="No recorded game found.")
            return

        if len(lines) == 0:
            self.statusLabel.config(text="Record file is empty.")
            return

        parts = lines[0].strip().split()
        self.replayBoardType = parts[0].strip().lower()
        self.replayBoardSize = int(parts[1].strip())
        self.replayMode = parts[2].strip().lower() if len(parts) > 2 else 'manual'

        self.replayMoves = []
        i = 1
        while i < len(lines):
            nums = lines[i].strip().split()
            if len(nums) == 6:
                move = (int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3]), int(nums[4]), int(nums[5]))
                self.replayMoves.append(move)
            i = i + 1

        if self.replayMode == 'manual':
            self.game = ManualGame(self.replayBoardType, self.replayBoardSize)
        else:
            self.game = AutoGame(self.replayBoardType, self.replayBoardSize)

        self.autoRunning = False
        self.replayRunning = True
        self.replayIndex = 0
        self.drawBoard()
        self.updateStatus()
        self.statusLabel.config(text="Replaying...")
        self.start.after(600, self.replayStep)

    def replayStep(self):
        if not self.replayRunning:
            return
        if self.replayIndex >= len(self.replayMoves):
            self.replayRunning = False
            if self.game.hasWon():
                self.statusLabel.config(text="Replay done. You won!")
            else:
                self.statusLabel.config(text="Replay done. " + str(self.game.pegCount) + " pegs remaining.")
            return
        move = self.replayMoves[self.replayIndex]
        self.replayIndex = self.replayIndex + 1
        size = len(self.game.board)
        fromR = move[0]
        fromC = move[1]
        toR = move[2]
        toC = move[3]
        midR = move[4]
        midC = move[5]
        allInBounds = (0 <= fromR < size and 0 <= fromC < size and
                       0 <= toR < size and 0 <= toC < size and
                       0 <= midR < size and 0 <= midC < size)
        if allInBounds:
            self.game.makeMove(fromR, fromC, toR, toC, midR, midC)
        self.drawBoard()
        self.updateStatus()
        self.start.after(600, self.replayStep)

    def drawBoard(self):
        for w in self.canvasFrame.winfo_children():
            w.destroy()

        self.cellPegs = []
        board = self.game.board
        gridSize = len(board)
        cellSize = 20
        canvasSize = gridSize * cellSize + 10

        self.canvas = tk.Canvas(self.canvasFrame, width=canvasSize, height=canvasSize)
        self.canvas.configure(highlightthickness=0)
        self.canvas.pack()

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
                elif cellState == 2:
                    peg = self.canvas.create_oval(centerX - radius, centerY - radius, centerX + radius, centerY + radius)
                    self.canvas.itemconfig(peg, fill='white', outline='black', width=1)
                    pegRow.append(peg)

                column = column + 1
            self.cellPegs.append(pegRow)
            row = row + 1

        self.canvas.bind('<Button-1>', self.onClick)

    def onClick(self, event):
        if not isinstance(self.game, ManualGame):
            return
        if self.game.isGameOver():
            return
        if self.replayRunning:
            return

        cellSize = 20
        col = (event.x - 1) // cellSize
        row = (event.y - 1) // cellSize

        if row < 0 or row >= self.game.boardSize or col < 0 or col >= self.game.boardSize:
            return

        if self.game.selectedPeg is None:
            self.game.selectPeg(row, col)
            self.drawBoard()
            if self.game.selectedPeg is not None:
                self.highlightMoves()
        else:
            lastMove = self.game.moveCount
            if self.game.tryMove(row, col):
                h = self.game.moveHistory
                if len(h) > 0:
                    m = h[len(h) - 1]
                    self.writeMove(m[0], m[1], m[2], m[3], m[4], m[5])
                self.drawBoard()
                self.updateStatus()
                if self.game.isGameOver():
                    self.showGameOver()
            else:
                self.game.selectPeg(row, col)
                self.drawBoard()
                if self.game.selectedPeg is not None:
                    self.highlightMoves()

    def highlightMoves(self):
        if self.game.selectedPeg is None:
            return
        cellSize = 20
        r = self.game.selectedPeg[0]
        c = self.game.selectedPeg[1]
        x1 = c * cellSize + 1
        y1 = r * cellSize + 1
        x2 = x1 + cellSize
        y2 = y1 + cellSize
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='blue', width=2)

        i = 0
        while i < len(self.game.validMoves):
            m = self.game.validMoves[i]
            mr = m[0]
            mc = m[1]
            mx1 = mc * cellSize + 1
            my1 = mr * cellSize + 1
            mx2 = mx1 + cellSize
            my2 = my1 + cellSize
            self.canvas.create_rectangle(mx1, my1, mx2, my2, outline='green', width=2)
            i = i + 1

    def autoplay(self):
        if isinstance(self.game, AutoGame):
            self.autoRunning = True
            self.runAutoStep()

    def runAutoStep(self):
        if not self.autoRunning:
            return
        if self.game.isGameOver():
            self.showGameOver()
            return
        self.game.autoStep()
        h = self.game.moveHistory
        if len(h) > 0:
            m = h[len(h) - 1]
            self.writeMove(m[0], m[1], m[2], m[3], m[4], m[5])
        self.drawBoard()
        self.updateStatus()
        if self.game.isGameOver():
            self.showGameOver()
            return
        self.start.after(500, self.runAutoStep)

    def randomize(self):
        if isinstance(self.game, ManualGame):
            self.game.randomize()
            h = self.game.moveHistory
            if len(h) > 0:
                m = h[len(h) - 1]
                self.writeMove(m[0], m[1], m[2], m[3], m[4], m[5])
            self.drawBoard()
            self.updateStatus()
            if self.game.isGameOver():
                self.showGameOver()

    def undo(self):
        if self.game is not None:
            self.game.undoMove()
            if isinstance(self.game, ManualGame):
                self.game.selectedPeg = None
                self.game.validMoves = []
            self.drawBoard()
            self.updateStatus()

    def updateStatus(self):
        if self.game is not None:
            text = "Pegs: " + str(self.game.pegCount) + "  Moves: " + str(self.game.moveCount)
            self.statusLabel.config(text=text)

    def showGameOver(self):
        self.autoRunning = False
        if self.game.hasWon():
            self.statusLabel.config(text="You won! Only 1 peg left!")
        else:
            text = "Game over. " + str(self.game.pegCount) + " pegs remaining."
            self.statusLabel.config(text=text)


if __name__ == "__main__":
    start = tk.Tk()
    game = SolitaireGame(start)
    start.mainloop()
