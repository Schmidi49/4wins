import numpy as np

ROWS = 6
COLS = 7
PVE = 0

def setup(rows = 6, cols = 7, pve = 0):
    global ROWS, COLS, PVE
    ROWS = rows
    COLS = cols
    PVE = pve


class state:
    field = np.ndarray(shape=(COLS, ROWS), dtype=int)
    result = False
    moveList = []
    onTurn = -1

    def check(self, pos):
        if len(self.moveList) == ROWS * COLS:
            result = 0
            return True
        if self.checkHor(pos[1]):
            return True
        elif self.checkVer(pos[0]):
            return True
        elif self.checkDiaL(pos[1],pos[0]):
            return True
        elif self.checkDiaR(pos[1],pos[0]):
            return True
        return False

    def __init__(self):
        self.field.resize(COLS, ROWS, refcheck=False)
        self.field.fill(0)
        self.result = False
        self.moveList.clear
        onTurn = -1

    def executeGame(self, multiMoves):
        for singleMove in multiMoves:
            print(singleMove)
            turn = False
            try:
                turn = self.move(singleMove)
            except ValueError:
                print("Input can only be an integer!")
            if turn:
                if self.check(turn):
                    break

    def move(self, col):
        col %= COLS
        for i in range(ROWS):
            if self.field[col][i] == 0:
                self.field[col][i] = -self.onTurn
                self.moveList.append(col)
                self.onTurn = -self.onTurn
                return [col, i]
        return False

    def back(self):
        try:
            for i in range(ROWS-1,0):
                if self.field[self.moveList[-1]][i] is not 0:
                    self.field[self.moveList[-1]][i] = 0
                    self.moveList.pop(-1)
                    self.onTurn=-self.onTurn
                    return
        except LookupError:
            print("No removeable error")


    def getMove(self, col):
        col %= COLS
        for i in range(ROWS):
            if self.field[col][i] == 0:
                return [col, i]
        return False

    def genMoves(self):
        moves = []
        for i in range(COLS):
            if self.field[i][ROWS-1] == 0:
                moves.append(i)

    def checkHor(self, row):
        count = 0
        for i in range(COLS):
            if self.field[i][row] == self.onTurn:
                count +=1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count=0
        return False

    def checkVer(self, col):
        count = 0
        for i in range(ROWS):
            if self.field[col][i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
        return False

    def checkDiaR(self, row, col):
        count = 0
        if col > (ROWS - 1 - row):
            start = ROWS - 1 - row
        else:
            start = col
        i = 0
        while (row + start - i) > -1 and (col - start + i) < COLS:
            if self.field[col - start + i][row + start - i] == self.onTurn:
                count += 1
                if count == 4:
                    self.result = self.onTurn
                    return self.onTurn
            else:
                count = 0
            i+=1
        return False

    def checkDiaL(self, row, col):
        count = 0
        if (ROWS - 1 - row) > (COLS - 1 - col):
            start = COLS - 1 - col
        else:
            start = ROWS - 1 - row
        i = 0
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