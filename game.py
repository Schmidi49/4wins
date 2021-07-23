import numpy as np

'''
for every gamestate of a game, the number of coulombs, rows and the gamemode must be the same
PVE safe which player is the computer, either 1 or 2
if PVE is 0, both players are human (default)
'''
ROWS = 6
COLS = 7
PVE = 0


# setups the program to either start a game or include the engine
def setup(rows=6, cols=7, pve=0):
    global ROWS, COLS, PVE
    ROWS = rows
    COLS = cols
    PVE = pve


'''
each state is a unique gamestate on a board
they can be different in playing field, in the move list etc.
'''


class State:
    # the field contains each square of the field
    # 0 are empty squares, 1 and -1 represent the stones of each player
    field = np.ndarray(shape=(COLS, ROWS), dtype=int)
    # the result is either false if the game is in progress, 0 for draw or 1/-1 which signals a win
    result = False
    # contains all executed moves of the gamestate
    moveList = []
    # signals which player is currently on turn (a player is on turn until the move of the next one is executed!)
    onTurn = -1

    # if a new instance of the class is created, all variables are cleared
    def __init__(self, startturns=[]):
        self.field.resize(COLS, ROWS, refcheck=False)
        self.field.fill(0)
        self.result = False
        self.moveList.clear
        onTurn = -1
        self.executeGame(startturns)

    '''
    calls all individual check function
    (all of them search for a row of 4 in a certain direction)
    additionally it checks if all squares are used and the game is a draw
    the position of the last move must be in the argument (Format: [col,row]) to lower the calculation time
    '''

    def check(self, pos):
        if self.checkHor(pos):
            return True
        elif self.checkVer(pos):
            return True
        elif self.checkDiaL(pos):
            return True
        elif self.checkDiaR(pos):
            return True
        elif len(self.moveList) == ROWS * COLS:
            self.result = 0
            return True
        return False

    # adds a move to the gamestate and returns the exact used square of the move
    def move(self, col):
        col %= COLS
        for i in range(ROWS):
            if self.field[col][i] == 0:
                self.field[col][i] = -self.onTurn
                self.moveList.append(col)
                self.onTurn = -self.onTurn
                return [col, i]
        return False

    # just gets the position of a possible move without executing it
    def getMove(self, col):
        col %= COLS
        for i in range(ROWS):
            if self.field[col][i] == 0:
                return [col, i]
        return False

    # executes multiple moves at once
    def executeGame(self, multiMoves):
        for singleMove in multiMoves:
            turn = False
            try:
                turn = self.move(singleMove)
            except ValueError:
                print("Input can only be an integer!")
            if turn:
                if self.check(turn):
                    break

    # deletes the last few move
    def back(self, count=1):
        for j in range(count):
            # safety tool, if more moves than possible are deletet
            try:
                for i in range(1, ROWS + 1):
                    if self.field[self.moveList[-1]][ROWS - i] != 0:
                        self.field[self.moveList[-1]][ROWS - i] = 0
                        self.moveList.pop(-1)
                        self.onTurn = -self.onTurn
                        break
            except IndexError:
                print("No more move to delete")
                return

    # generates a list of all currently possible moves by looking into the top-square
    def genMoves(self):
        moves = []
        for i in range(COLS):
            if self.field[i][ROWS - 1] == 0:
                moves.append(i)
        return moves

    # checks for a horizontal line of 4 (from the field of the move down 4 Tiles)
    def checkHor(self, pos):
        if (pos[1] > 2):
            if 4 * self.onTurn == self.field[pos[0]][pos[1] - 0] + self.field[pos[0]][pos[1] - 1] + self.field[pos[0]][
                pos[1] - 2] + self.field[pos[0]][pos[1] - 3]:
                self.result = self.onTurn
                return True
        return False

    # checks for a vertical line of 4 (only the coulomb of the executed move)
    # additionally, only the 3 tiles before and after the current tile get checked
    def checkVer(self, pos):
        count = 0
        # check every square of the coulomb
        for i in range(0 if (pos[0] - 3) < 0 else (pos[0] - 3), COLS if (pos[0] + 4) > COLS else (pos[0] + 4)):
            '''
            if the square belongs the current player on turn, count up
            if the counter reaches 4 -> player won
            if there is an enemy or empty field in between -> reset the counter
            '''
            if self.field[i][pos[1]] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
        return False

    # checks for a diagonal line of 4 (only the diagonal to the upper right corner which contains the current move)
    # additionally, only the 3 tiles before and after the current tile get checked
    def checkDiaR(self, pos):
        count = 0
        i = -pos[0] if pos[0] < pos[1] else -pos[1]  # set the increment to the lower of the positions
        if i < -3:
            i = -3
        # check until 4 tiles after current move or out of bounds
        while i < 4 and (pos[0] + i) < COLS and (pos[1] + i) < ROWS:
            if (self.field[pos[0] + i][pos[1] + i] == self.onTurn):
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return True
            else:
                count = 0
            i += 1

        return False

    # checks for a diagonal line of 4 (only the diagonal to the upper left corner which contains the current move)
    # additionally, only the 3 tiles before and after the current tile get checked
    def checkDiaL(self, pos):
        count = 0
        # set the increment to the lower delta to the down right border
        i = pos[0] - ROWS if ROWS - pos[0] < pos[1] else -pos[1]
        if i < -3:
            i = -3
        # check until 4 tiles after current move or out of bounds
        while i < 4 and (pos[0] - i) >= 0 and (pos[1] + i) < ROWS:
            if self.field[pos[0] - i][pos[1] + i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return True
            else:
                count = 0
            i += 1

        return False