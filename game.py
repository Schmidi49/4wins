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
    def __init__(self,startturns=[]):
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
        if self.checkHor(pos[1]):
            return True
        elif self.checkVer(pos[0]):
            return True
        elif self.checkDiaL(pos[1], pos[0]):
            return True
        elif self.checkDiaR(pos[1], pos[0]):
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
    def back(self, count = 1):
        for j in range(count):
            #safety tool, if more moves than possible are deletet
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

    # checks for a horizontal line of 4 (only the row of the executed move)
    def checkHor(self, row):
        count = 0
        # check every square in the row
        for i in range(COLS):
            '''
            if the square belongs the current player on turn, count up
            if the counter reaches 4 -> player won
            if there is an enemy or empty field in between -> reset the counter
            '''
            if self.field[i][row] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
        return False

    # checks for a vertical line of 4 (only the coulomb of the executed move)
    def checkVer(self, col):
        count = 0
        # check every square of the coulomb
        for i in range(ROWS):
            '''
            if the square belongs the current player on turn, count up
            if the counter reaches 4 -> player won
            if there is an enemy or empty field in between -> reset the counter
            '''
            if self.field[col][i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
        return False

    # checks for a diagonal line of 4 (only the diagonal to the down right which contains the current move)
    def checkDiaR(self, row, col):
        count = 0
        # checks if the start square of the diagonal is ont vertical or horizontal border
        if col > (ROWS - 1 - row):
            start = ROWS - 1 - row
        else:
            start = col
        i = 0
        '''
        from then on go threw each square of the diagonal
        if the counter reaches 4 -> player won
        if there is an enemy or empty field in between -> reset the counter
        '''
        while (row + start - i) > -1 and (col - start + i) < COLS:
            if self.field[col - start + i][row + start - i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
            i += 1
        return False

    # checks for a diagonal line of 4 (only the diagonal to the down left which contains the current move)
    def checkDiaL(self, row, col):
        count = 0
        # checks if the start square of the diagonal is ont vertical or horizontal border
        if (ROWS - 1 - row) > (COLS - 1 - col):
            start = COLS - 1 - col
        else:
            start = ROWS - 1 - row
        i = 0
        '''
        from then on go threw each square of the diagonal
        if the counter reaches 4 -> player won
        if there is an enemy or empty field in between -> reset the counter
        '''
        while (row + start - i) > -1 and (col + start - i) > -1:
            if self.field[col + start - i][row + start - i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
            i += 1
        return False
