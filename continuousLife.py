import random
from tkinter import *

MAX_UPDATE = 0.5
INFLUENCE_RADIUS = 2
OPTIMUM_VALUE = 0.375
HARSHNESS_VALUE = 3
WIDTH = 50
HEIGHT = 50
CELL_SIZE = 15
FRAME_DELAY = 20

def updateFunction(displacement):
    return (-(HARSHNESS_VALUE/OPTIMUM_VALUE) * displacement + 1) * MAX_UPDATE

class Cell:
    def __init__(self, position, value, colour):
        self.position = position
        self.value = value
        self.colour = colour
        maxColour = max(self.colour)
        if maxColour != 0:
            for colour in self.colour: colour /= maxColour

    def updateColour(self, colourSum):
        maxColour = max(colourSum)
        if maxColour != 0:
            for i in range(len(colourSum)): colourSum[i] /= maxColour
        self.colour = colourSum
        
    def getColour(self):
        rgbColour = self.colour.copy()
        for i, colour in enumerate(rgbColour):
            colour = hex(int(self.value * colour * 255))[2:4]
            if len(colour) == 1: colour = "0" + colour
            rgbColour[i] = colour
        return f"#{rgbColour[0]}{rgbColour[1]}{rgbColour[2]}"

    def update(self, board):
        neighbourSum = 0
        colourSum = [0, 0, 0]
        for i in range(-INFLUENCE_RADIUS, INFLUENCE_RADIUS + 1):
            for j in range(-INFLUENCE_RADIUS, INFLUENCE_RADIUS + 1):
                if i + self.position[0] > 0 and i + self.position[0] < HEIGHT and j + self.position[1] > 0 and j + self.position[1] < WIDTH and not self.position == (i, j):
                    neighbourSum += board[i + self.position[0]][j + self.position[1]].value
                    for k in range(3): colourSum[k] += board[i + self.position[0]][j + self.position[1]].colour[k] * board[i + self.position[0]][j + self.position[1]].value
        self.updateColour(colourSum)
        neighbourValue = neighbourSum / ((INFLUENCE_RADIUS + 1) ** 2 - 1)
        displacement = abs(neighbourValue - OPTIMUM_VALUE)
        updateValue = updateFunction(displacement) + self.value
        if updateValue > 1: return 1
        if updateValue < 0: return 0
        return updateValue

def nextTurn(board):
    canvas.delete(ALL)
    boardClone = [[] for _ in range(HEIGHT)]
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            boardClone[i].append(Cell((i,j), cell.update(board), cell.colour))
    board = boardClone
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell.value != 0:
                canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE, j * CELL_SIZE + CELL_SIZE, i * CELL_SIZE + CELL_SIZE, fill=cell.getColour(), outline="")
    window.after(FRAME_DELAY, nextTurn, board)
    
board = [[Cell((j, i), 0, [0, 0, 0]) for j in range(WIDTH)] for i in range(HEIGHT)]
for _ in range(HEIGHT * WIDTH // 30):
    y = random.randint(0, HEIGHT - 1)
    x = random.randint(0, WIDTH - 1)
    board[y][x] = Cell((y, x), 1, [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])

window = Tk()
window.title("Continuous")
window.resizable(False, False)
canvas = Canvas(window, bg="#000000", height=HEIGHT * CELL_SIZE, width=WIDTH * CELL_SIZE)
canvas.pack(padx=10, pady=10)
window.update()

nextTurn(board)
window.mainloop()
