import numpy as np

field = np.ndarray(shape=(7,6), dtype= int)
result = 0
moveList = []

def check(pos):
    global result
    if len(moveList) == 42:
        result = 3
        return True
    if checkHor(pos[0]):
        return True
    elif checkVer(pos[1]):
        return True
    elif checkDiaL(pos[0],pos[1]):
        return True
    elif checkDiaR(pos[0],pos[1]):
        return True
    return False

def newGame():
    field.fill(0)
    result = 0
    moveList.clear()

def executeGame(multiMoves):
    for singleMove in multiMoves:
        turn = False
        try:
            turn = move(singleMove)
        except ValueError:
            print("Input can only be an integer!")
        if turn:
            if check(turn):
                break

def move(col):
    col %= 7
    for i in range(6):
        if field[col][i] == 0:
            field[col][i] = (len(moveList)%2) + 1
            moveList.append(col)

            return [i, col]
    return False

def checkHor(row):
    global result
    onTurn = ((len(moveList) - 1) % 2) + 1
    count = 0
    for i in range(7):
        if field[i][row] == onTurn:
            count +=1
            if count == 4:
                result = onTurn
                return onTurn
        else:
            count=0
    return False

def checkVer(col):
    global result
    onTurn = ((len(moveList) - 1) % 2) + 1
    count = 0
    for i in range(6):
        if field[col][i] == onTurn:
            count += 1
            if count == 4:
                result = onTurn
                return onTurn
        else:
            count = 0
    return False

def checkDiaR(row,col):
    global result
    onTurn = ((len(moveList) - 1) % 2) + 1
    count = 0
    if col > (5 - row):
        start = 5 - row
    else:
        start = col
    i = 0
    while (row + start - i) > -1 and (col - start + i) < 7:
        if field[col - start + i][row + start - i] == onTurn:
            count += 1
            if count == 4:
                result = onTurn
                return onTurn
        else:
            count = 0
        i+=1
    return False

def checkDiaL(row,col):
    global result
    onTurn = ((len(moveList) - 1) % 2) + 1
    count = 0
    if (5 - row) > (6 - col):
        start = 6 - col
    else:
        start = 5 - row
    i = 0
    while (row + start - i) > -1 and (col + start - i) > -1:
        if field[col + start - i][row + start - i] == onTurn:
            count += 1
            if count == 4:
                result = onTurn
                return onTurn
        else:
            count = 0
        i += 1
    return False