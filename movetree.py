class Tree:
    def __init__(self, moves=[], value=None):
        self.value = value
        self.branch = {}
        for move in moves:
            self.branch[move] = None


    def endres(self, value):
        for limb in self.branch:
            self.branch[limb] = Tree(value=value)
        return self

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

    def getBranch(self, notation):
        if notation:
            try:
                return self.branch[notation[0]].getBranch(notation[1:])
            except KeyError:
                print("Move not accessible")
                return self
        else:
            return self


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
