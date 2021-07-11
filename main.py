import sys
import prnt
import game
# import evaluation as ev


def ui(rows=6, cols=7, pve=0):
    rows = int(rows)
    cols = int(cols)
    if not ((pve == 0) | (pve == 1) | (pve == 2)):
        pve = 0
    game.setup(rows, cols, pve)
    curGame = game.state()

    turn = False
    while True:
        prnt.board(curGame.field)
        try:
            turn = curGame.move(int(input("Zug: ")))
        except ValueError:
            print("Input can only be an integer!")
        if turn:
            if curGame.check(turn):
                prnt.board(curGame.field)
                if curGame.result == 1:
                    print("Player 1 won!")
                elif curGame.result == -1:
                    print("Player 2 won!")
                elif curGame.result == 0:
                    print("curGame ended in Draw")
                break
    print(curGame.moveList)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3:
        ui()
    elif len(sys.argv) > 4:
        ui(sys.argv[2], sys.argv[1], sys.argv[3])
    else:
        ui(sys.argv[2], sys.argv[1])
