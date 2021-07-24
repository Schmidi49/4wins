"""
the engine is the computer, which calculates moves
it works mainly with trees to see in advance, until a certain threshold, where the value of the positions are meassured
and the best move is calculated
"""
import movetree as mt

# multiplier of actual possible chances, see evaluate() for nearer information
MULTPOT = 4
# !ADDITIONAL! points, if some stones are in the inner center
MULTCEN = 3

def genTree(gamestate, depth, order=0):
    """
    generates a blank tree from a certain position with a certain depth
    :param gamestate: the gamestate from which the tree should be createt
    :param depth: how many moves deep deep the tree should go
    :param order: internal variable for recursion, to know on which depth the tree is already
    :return: full grown movetree in form of a non binary Tree
    """
    if order < depth:
        root = mt.Tree(gamestate.genMoves())
        for limb in root.branch:
            ge = gamestate.check(gamestate.move(limb))
            if ge:
                root.branch[limb] = mt.Tree(value=gamestate.result)
                gamestate.result = None
            else:
                root.branch[limb] = genTree(gamestate, depth, order + 1)
            gamestate.back()
        return root


def genCalcedTree(gamestate, depth, order=0):
    """
    TODO
    :param gamestate: the gamestate from which the tree should be created
    :param depth: how many moves deep deep the tree should go
    :param order: internal variable for recursion, to know on which depth the tree is already
    :return: TODO
    """
    pass

def evaluate(gamestate):
    """
    a position is good, when there is marging for error and there is playmaking potential:
    both can be seen in a position, which allows, even if just theoretical, to end on many different fields
    therefore 2 parameters are measured: primarily the potential for ending, secondary the stones in the center
    the weights works by heavily multiplying the values, while a centered is worth 1 point, the potential to end is worth
    1000 points (a win is always better and worth 1M points)
    stones in center are a symptom for a good position, the result is a potential to end, therefore the weight
    1 appart form the brder are worth one point, if the stone is 2 or more appart, its worth additional points
    :param gamestate: the gamestate which should be evaluated
    :return: value of the position
    """
    cols = gamestate.cols()
    rows = gamestate.rows()

    # save of the onTurn, cause evaluated messes with the gamestate and it has to be reseted, cause State is Mutable
    save = gamestate.onTurn
    # value of the position
    value = 0
    # instant value centerpieces
    for i in range(1, cols - 1):
        for j in range(1, rows - 1):
            value += gamestate.field[i][j]
    for i in range(2, cols - 2):
        for j in range(2, rows - 2):
            value += MULTCEN * gamestate.field[i][j]

    # height-profile of the columns
    height = []
    # internal variable
    cur = 0
    # calc height-profile coulomb by coulomb
    for i in range(cols):
        for j in range(rows):
            cur = gamestate.field[i][j]
            if cur == 0:
                height.append(j)
                break
        if cur != 0:
            height.append(rows)
            cur = 0

    """
    the second, but heavier-weighted methode for evaluating are the potential chances
    so the margin of error or the potential for playmaking is measured
    actual winning moves (directly the height) are worth MULTPOT (scalable factor) times the points
    """

    # first col has to be separated due to overflows
    value += MULTPOT * potWin(gamestate, [0, height[0]])
    if height[1] < height[0]:
        for j in range(height[1] + 1, height[0] + 1):
            value += potWin(gamestate, [1, j])
    # first checks the direct height of the cols, then goes up or down towards the nex one to cover every border-field
    for i in range(1, (cols - 1)):
        value += MULTPOT * potWin(gamestate, [i, height[i]])
        if height[i + 1] < height[i]:
            for j in range(height[i + 1] + 1, height[i] + 1):
                value += potWin(gamestate, [i + 1, j])
        if height[i + 1] > height[i] and height[i + 1] > height[i - 1]:
            for j in range(height[i] + 1, height[i + 1] + 1):
                value += potWin(gamestate, [i, j])
    # last col has to be separated due to overflows
    value += MULTPOT * potWin(gamestate, [cols - 1, height[cols - 1]])

    # resets the onTurn, cause State is Mutable
    gamestate.onTurn = save
    return value


def potWin(gamestate, pos):
    """
    searches on a certain square for a win by using in the State included check-function
    :param gamestate: state on which the check is made
    :param pos: square on which the check is made
    :return: value of this exact squre
    """
    if pos[1] != gamestate.rows():
        value = 0
        gamestate.field[pos[0]][pos[1]] = 1
        gamestate.onTurn = 1
        if gamestate.check(pos):
            if gamestate.result != 0:
                value += 1000
            gamestate.result = False
        gamestate.field[pos[0]][pos[1]] = -1
        gamestate.onTurn = -1
        if gamestate.check(pos):
            if gamestate.result != 0:
                value -= 1000
            gamestate.result = False

        # gamestate has to be soft-reseted, cause State is a Mutable-object
        gamestate.field[pos[0]][pos[1]] = 0
        return value
    return 0

#testing function
if __name__ == '__main__':
    import game
    import prnt

    game.setup()
    cur = game.State()

    cur.field[3][0] = 1
    cur.field[3][1] = 1
    cur.field[3][2] = 1
    cur.field[4][2] = 1
    cur.field[5][2] = 1
    cur.field[4][0] = -1
    cur.field[4][1] = -1
    cur.field[5][0] = -1
    cur.field[5][1] = -1

    prnt.board(cur.field)
    print(evaluate(cur))
