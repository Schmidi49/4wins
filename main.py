import prnt
import engine as eg
import evaluation as ev

def UI():
    eg.newGame()
    turn = False
    while True:
        prnt.board(eg.field)
        try:
            turn = eg.move(int(input("Zug: ")))
        except ValueError:
            print("Input can only be an integer!")
        if turn:
            if eg.check(turn):
                prnt.board(eg.field)
                if eg.result == 1:
                    print("Player 1 won!")
                elif eg.result == 2:
                    print("Player 2 won!")
                elif eg.result == 3:
                    print("Game ended in Draw")
                break







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UI()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
