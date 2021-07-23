"""
example of the backend-modules used to create a UI
TODO: can be used in both modes, PvP and PvE
"""
import sys
import prnt
import game
import engine

# import evaluation as ev


def ui(rows=6, cols=7, pve=0):
    """
    converts arguments into usable data
    :param rows: number of wanted rows, on default 6
    :param cols: number of wanted coulombs, on default 7
    :param pve: used mode, if 0 its PvP, if its 1 or -1, called player is played by the engine
    :return: None
    """
    rows = int(rows)
    cols = int(cols)
    if not ((pve == 0) | (pve == 1) | (pve == 2)):
        pve = 0
    game.setup(rows, cols, pve)

    # setup a gamestate, which is the current game
    curGame = game.State()

    '''
    turn is the returned value of the check-function
    if the return is false, the gamestate isn't over
    if the value is true, there is a result (win, draw or lose)
    '''
    turn = False

    while True:
        # prints the board
        prnt.board(curGame.field)
        # only except ints as valid inputs

        # FOR DEBUGGING
        engine.evaluate(curGame)

        try:
            turn = curGame.move(int(input("Zug: ")))
        except ValueError:
            print("Input can only be an integer!")

        # if there is an result, inform the user
        if turn:
            if curGame.check(turn):
                prnt.board(curGame.field)
                if curGame.result == 1 * game.WIN:
                    print("Player 1 won!")
                elif curGame.result == -1 * game.WIN:
                    print("Player 2 won!")
                elif curGame.result == 0:
                    print("Game ended in Draw")
                break
    # at the end of the game, print the list of executed moves
    print(curGame.moveList)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3:
        ui()
    elif len(sys.argv) > 4:
        ui(sys.argv[2], sys.argv[1], sys.argv[3])
    else:
        ui(sys.argv[2], sys.argv[1])
