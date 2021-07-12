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
    game.setup()
    cur = game.State()
    genTree(cur, int(sys.argv[1])).print()
    pass