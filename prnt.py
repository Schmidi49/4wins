def board(field):
    print(topFrame())
    for i in range(5):
        print(tableLine())
        print(tableLine(field.compress((5 - i) * [False] + [True],1)))
        print(tableLine())
        print(midFrame())
    print(tableLine())
    print(tableLine(field.compress([True], 1)))
    print(tableLine())
    print(botFrame())

def strboard(field):
    s = topFrame() + '\n'
    for i in range(5):
        s += tableLine() + '\n'
        s += tableLine(field.compress((5 - i) * [False] + [True],1)) + '\n'
        s += tableLine() + '\n'
        s += midFrame() + '\n'
    s += tableLine() + '\n'
    s += tableLine(field.compress([True], 1)) + '\n'
    s += tableLine() + '\n'
    s += botFrame() + '\n'
    return s

def tableLine(fieldLine = 7 * [0]):
    if ((len(fieldLine)) != 7):
        line = [' '] * 7
    else:
        line = []
        for num in fieldLine:
            if num == 1:
                line.append('X')
            elif num == 2:
                line.append('O')
            else:
                line.append(' ')
    s = '\u2551'
    for char in line:
        s += 3 * ' ' + char + 3 * ' ' + '\u2551'
    return s


def topFrame():
    s = '\u2554' + 7 * '\u2550'
    s += 6 * ('\u2566' + 7 * '\u2550')
    s += '\u2557'
    return s

def midFrame():
    s = '\u2560' + 7 * '\u2550'
    s += 6 * ('\u256C' + 7 * '\u2550')
    s += '\u2563'
    return s

def botFrame():
    s = '\u255A' + 7 * '\u2550'
    s += 6 * ('\u2569' + 7 * '\u2550')
    s += '\u255D'
    return s

