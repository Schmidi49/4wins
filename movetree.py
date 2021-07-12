'''
the Tree-class is a non-binary tree, which links a move to its possible successor
in addition, its possible to assign each unique move a value, for example the evaluation of the position
this vale is on default None, while the branch is  on default an empty dictionary (called branch)
the key of the branch are the moves and the value is, if assigned, the successor-Tree
'''
class Tree:
    # a new Tree can instantly be filled with moves or an value
    def __init__(self, moves=[], value=None):
        self.value = value
        self.branch = {}
        for move in moves:
            self.branch[move] = None

    # sets all Tree-values of all the successor-moves to an certain value
    def endres(self, value):
        for limb in self.branch:
            self.branch[limb] = Tree(value=value)
        return self

    '''
    prints the tree and all successors in a "List"-Format
    goes threw the successor-Trees with a recursive-Function
    every []-construct contains certain moves, which can contain successor-branches
    ':' signals, that a position is evaluated and the value is printed. No more successors are printed
    '''
    def print(self):
        if self.value:
            print(':', self.value, end='', sep='')
            return
        print('[', end='')
        for limb in self.branch:
            print(limb, end='')
            if self.branch[limb]:
                self.branch[limb].print()
            print(',', end='')
        print('\b', end='')
        print(']', end='')

    #easier access threw the branch constructs, returns the called Tree after x-moves
    def getBranch(self, notation):
        if notation:
            try:
                return self.branch[notation[0]].getBranch(notation[1:])
            # if there is an not notated move, the Tree at this position gets returned
            except KeyError:
                print("Move not accessible")
                return self
        else:
            return self

# test-tree
if __name__ == '__main__':
    root = Tree([1, 2, 3])
    root.branch[1] = Tree([2,3])
    root.branch[1].branch[2] = Tree([3])
    root.branch[1].branch[2].branch[3] = Tree([3]).endres(1)
    root.branch[1].branch[3] = Tree([2, 3])
    root.branch[1].branch[3].branch[2] = Tree([3]).endres(1)
    root.branch[1].branch[3].branch[3] = Tree([2]).endres(0)
    root.branch[2] = Tree([1, 3])
    root.branch[2].branch[1] = Tree([3])
    root.branch[2].branch[1].branch[3] = Tree([3]).endres(1)
    root.branch[2].branch[3] = Tree([1, 3])
    root.branch[2].branch[3].branch[1] = Tree([3]).endres(1)
    root.branch[2].branch[3].branch[3] = Tree([1]).endres(0)
    root.branch[3] = Tree([1, 2, 3])
    root.branch[3].branch[1] = Tree([2, 3])
    root.branch[3].branch[1].branch[2] = Tree([3]).endres(1)
    root.branch[3].branch[1].branch[3] = Tree(value=-1)
    root.branch[3].branch[2] = Tree([1,3])
    root.branch[3].branch[2].branch[3] = Tree(value=-1)
    root.branch[3].branch[2].branch[1] = Tree([3]).endres(1)
    root.branch[3].branch[3] = Tree(value=1)

    root.print()
    print()
    test = root.getBranch([1, 3, 2])
    test.print()
