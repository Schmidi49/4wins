import sys
import game
import movetree as mt
import prnt


def genTree(gamestate, depth, order=0):
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


if __name__ == '__main__':
    game.setup(4, 4)
    cur = game.State([0, 1, 1, 2, 2, 3, 2, 3, 0, 1, 0, 0])
    cur.onTurn *= -1  # fix for bs

    test=genTree(cur, 5)
    test.print()
    pass