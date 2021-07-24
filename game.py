"""
in the game-module is the whole ruleset of the game
its the only thing needed to play a game, every checking and saving is done here
one instance of game.py supports 1 field-size, but several possible gamestates
so for every gamestate of a game, the number of coulombs, rows and the gamemode must be the same
PVE safe which player is the computer, either 1 or -1
if PVE is 0, both players are human (default)
"""
import numpy as np

ROWS = 6
COLS = 7
PVE = 0

# value of victory
WIN = 10 ** 6


def setup(rows=6, cols=7, pve=0):
    """
    setups the program to either start a game or include the engine
    :param rows: number of wanted rows, on default 6
    :param cols: number of wanted coulombs, on default 7
    :param pve: used mode, if 0 its PvP, if its 1 or -1, called player is played by the engine
    :return: None
    """
    global ROWS, COLS, PVE
    ROWS = rows
    COLS = cols
    PVE = pve


class State:
    """
    each state is a unique gamestate on a board
    they can be different in playing field, in the move list etc.
    """
    # the field contains each square of the field
    # 0 are empty squares, 1 and -1 represent the stones of each player
    field = np.ndarray(shape=(COLS, ROWS), dtype=int)
    # the result is either false if the game is in progress, 0 for draw or 1/-1 which signals a win
    result = False
    # contains all executed moves of the gamestate
    moveList = []
    # signals which player is currently on turn (a player is on turn until the move of the next one is executed!)
    onTurn = -1

    # return the global variables, if only a gamestate is given to a function
    def rows(self):
        return ROWS

    def cols(self):
        return COLS
    def pve(self):
        return PVE
    def win(self):
        return WIN

    # if a new instance of the class is created, all variables are cleared
    def __init__(self, startturns=[]):
        """
        initializes the gameState and set it ups to work as expected
        :param startturns: u can pass a list of moves to start not by zero, but in a certain position
        """
        self.field.resize(COLS, ROWS, refcheck=False)
        self.field.fill(0)
        self.result = False
        self.moveList.clear
        onTurn = -1
        self.executeGame(startturns)

    def check(self, pos):
        """
        calls all individual check function
        (all of them search for a row of 4 in a certain direction)
        additionally it checks if all squares are used and the game is a draw
        :param pos: the position of the last move is passed (Format:[col,row]) to lower the calculation time
        :return: True if the game is finished, else false
        """
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

    def move(self, col):
        """
        adds a move to the gamestate and returns the exact used square of the move
        :param col: coulomb of the move
        :return: the actual field on which the stone landed (4 wins support gravity), or false if move is impossible
        """
        col %= COLS
        for i in range(ROWS):
            if self.field[col][i] == 0:
                self.field[col][i] = -self.onTurn
                self.moveList.append(col)
                self.onTurn = -self.onTurn
                return [col, i]
        return False

    def getMove(self, col):
        """
        just gets the position of a possible move without executing it
        :param col: coulomb of the move
        :return: the actual field on which the stone landed (4 wins support gravity), or false if move is impossible
        """
        col %= COLS
        for i in range(ROWS):
            if self.field[col][i] == 0:
                return [col, i]
        return False

    def executeGame(self, multiMoves):
        """
        executes multiple moves at once
        :param multiMoves: list of moves to execute
        :return: None
        """
        for singleMove in multiMoves:
            turn = False
            try:
                turn = self.move(singleMove)
            except ValueError:
                print("Input can only be an integer!")
            if turn:
                if self.check(turn):
                    break

    def back(self, count=1):
        """
        deletes the last few move
        :param count: how many move are getting deleted
        :return: True if successful, False if an error occurred
        """
        for j in range(count):
            # safety tool, if more moves than possible are deleted
            try:
                for i in range(1, ROWS + 1):
                    if self.field[self.moveList[-1]][ROWS - i] != 0:
                        self.field[self.moveList[-1]][ROWS - i] = 0
                        self.moveList.pop(-1)
                        self.onTurn = -self.onTurn
                        break
            except IndexError:
                print("No more move to delete")
                return False
        self.result = 0
        return True

    def genMoves(self):
        """
        generates a list of all currently possible moves by looking into the top-square
        :return:
        """
        moves = []
        for i in range(COLS):
            if self.field[i][ROWS - 1] == 0:
                moves.append(i)
        return moves

    def checkHor(self, pos):
        """
        checks for a horizontal line of 4 (from the field of the move down 4 fields)
        :param pos: the position of the last move is passed (Format:[col,row]) to lower the calculation time
        :return: True if the game is finished, else false:
        """
        if (pos[1] > 2):
            if 4 * self.onTurn == self.field[pos[0]][pos[1] - 0] + self.field[pos[0]][pos[1] - 1] + \
                    self.field[pos[0]][pos[1] - 2] + self.field[pos[0]][pos[1] - 3]:
                self.result = self.onTurn * WIN
                return True
        return False

    def checkVer(self, pos):
        """
        checks for a vertical line of 4 (only the coulomb of the executed move)
        additionally, only the 3 field before and after the current field get checked
        :param pos: the position of the last move is passed (Format:[col,row]) to lower the calculation time
        :return: True if the game is finished, else false
        """
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
                    self.result = self.onTurn * WIN
                    return True
            else:
                count = 0
        return False

    def checkDiaR(self, pos):
        """
        checks for a diagonal line of 4 (only the diagonal to the upper right corner which contains the current move)
        additionally, only the 3 field before and after the current field get checked
        :param pos: the position of the last move is passed (Format:[col,row]) to lower the calculation time
        :return: True if the game is finished, else false
        """
        count = 0
        i = -pos[0] if pos[0] < pos[1] else -pos[1]  # set the increment to the lower of the positions
        if i < -3:
            i = -3
        # check until 4 field after current move or out of bounds
        while i < 4 and (pos[0] + i) < COLS and (pos[1] + i) < ROWS:
            if (self.field[pos[0] + i][pos[1] + i] == self.onTurn):
                count += 1
                if count == 4:
                    self.result = self.onTurn * WIN
                    return True
            else:
                count = 0
            i += 1

        return False

    def checkDiaL(self, pos):
        """
        checks for a diagonal line of 4 (only the diagonal to the upper left corner which contains the current move)
        additionally, only the 3 field before and after the current field get checked
        :param pos: the position of the last move is passed (Format:[col,row]) to lower the calculation time
        :return: True if the game is finished, else false
        """
        count = 0
        # set the increment to the lower delta to the down right border
        i = pos[0] - ROWS if ROWS - pos[0] < pos[1] else -pos[1]
        if i < -3:
            i = -3
        # check until 4 field after current move or out of bounds
        while i < 4 and (pos[0] - i) >= 0 and (pos[1] + i) < ROWS:
            if self.field[pos[0] - i][pos[1] + i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn * WIN
                    return True
            else:
                count = 0
            i += 1

        return False
