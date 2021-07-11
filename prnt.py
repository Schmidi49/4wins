def board(field):
    cols = len(field)
    rows = len(field.compress([True],0).flat)
    print(topFrame(cols))
    for i in range(rows - 1):
        print(tableLine(cols * [0]))
        print(tableLine(field.compress((rows - 1 - i) * [False] + [True],1)))
        print(tableLine(cols * [0]))
        print(midFrame(cols))
    print(tableLine(cols * [0]))
    print(tableLine(field.compress([True], 1)))
    print(tableLine(cols * [0]))
    print(botFrame(cols))

def strboard(field):
    s = topFrame() + '\n'
    cols = len(field)
    rows = len(field.compress([True],0).flat)
    s += topFrame(cols)
    for i in range(rows - 2):
        s += tableLine(cols * [0])
        s += tableLine(field.compress((rows - 1 - i) * [False] + [True],1))
        s += tableLine(cols * [0])
        s += midFrame(cols)
    s += tableLine(cols * [0])
    s += tableLine(field.compress([True], 1))
    s += tableLine(cols * [0])
    s += botFrame(cols)
    return s

def tableLine(fieldLine = 7 * [0]):
    line = []
    for num in fieldLine:
        if num == 1:
            line.append('X')
        elif num == -1:
            line.append('O')
        else:
            line.append(' ')
    s = '\u2551'
    for char in line:
        s += 3 * ' ' + char + 3 * ' ' + '\u2551'
    return s


def topFrame(cols):
    s = '\u2554' + 7 * '\u2550'
    s += (cols - 1) * ('\u2566' + 7 * '\u2550')
    s += '\u2557'
    return s

def midFrame(cols):
    s = '\u2560' + 7 * '\u2550'
    s += (cols - 1) * ('\u256C' + 7 * '\u2550')
    s += '\u2563'
    return s

def botFrame(cols):
    s = '\u255A' + 7 * '\u2550'
    s += (cols - 1) * ('\u2569' + 7 * '\u2550')
    s += '\u255D'
    return s

