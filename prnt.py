"""
this function exist to visualize the field by an ASCII table
the table consist of 5 different types of lines
1) the top frame: looks like the following: ╔═══╦═══╗
2) the horizontal frames:                     ╠═══╬═══╣
3) the bottom frame:                        ╚═══╩═══╝
4) the in-between-lines: to make it more appealing for the human eye, there are in between line,
  which only contain the vertical lines:    ║   ║   ║
  (these are generated by making a data-line with no data, so there are only spaces)
5) and last the data lines: these make the 1s or -1 in the squares to Xes or Os
therefore, to print the board, a field must be transmitted
for example, a board can look like this:
╔═══════╦═══════╦═══════╦═══════╗
║       ║       ║       ║       ║
║       ║       ║       ║       ║
║       ║       ║       ║       ║
╠═══════╬═══════╬═══════╬═══════╣
║       ║       ║       ║       ║
║       ║       ║   X   ║       ║
║       ║       ║       ║       ║
╠═══════╬═══════╬═══════╬═══════╣
║       ║       ║       ║       ║
║   O   ║       ║   X   ║       ║
║       ║       ║       ║       ║
╠═══════╬═══════╬═══════╬═══════╣
║       ║       ║       ║       ║
║   O   ║   X   ║   O   ║       ║
║       ║       ║       ║       ║
╚═══════╩═══════╩═══════╩═══════╝
"""


def board(field):
    """
    prints the board on the console
    :param field: the field which should get printed on the console
    :return: None
    """
    # get the number of rows and coulombs to generate the right sized table
    cols = len(field)
    rows = len(field.compress([True], 0).flat)
    # print the top frames
    print(topFrame(cols))
    # then, for every row but the last, print 1 in-between line, 1 data line, 1 in-between line and a horizontal frame
    for i in range(rows - 1):
        print(tableLine(cols * [0]))
        print(tableLine(field.compress((rows - 1 - i) * [False] + [True], 1)))
        print(tableLine(cols * [0]))
        print(midFrame(cols))
    # for the last row, the vertical frame is a bottom frame
    print(tableLine(cols * [0]))
    print(tableLine(field.compress([True], 1)))
    print(tableLine(cols * [0]))
    print(botFrame(cols))


def strboard(field):
    """
    returns the complete string of the board
    :param field: the field which should get printed on the console
    :return: None
    """
    cols = len(field)
    rows = len(field.compress([True], 0).flat)
    s = topFrame(cols) + '\n'
    for i in range(rows - 2):
        s += tableLine(cols * [0]) + '\n'
        s += tableLine(field.compress((rows - 1 - i) * [False] + [True], 1)) + '\n'
        s += tableLine(cols * [0]) + '\n'
        s += midFrame(cols) + '\n'
    s += tableLine(cols * [0]) + '\n'
    s += tableLine(field.compress([True], 1)) + '\n'
    s += tableLine(cols * [0]) + '\n'
    s += botFrame(cols) + '\n'
    return s


def tableLine(fieldLine=7 * [0]):
    """
    prints col-times a vertical frame, some space, the looks up the square and prints the symbol
    if nothing is passed, returns an empty Line with only between-lines
    :param fieldLine: a single, horizontal Line of the Field
    :return: ASCII-string of the line
    """
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
    """
    the top frame is relatively static, only repeated col-times
    :param cols: number of coulombs
    :return: ASCII-string of the line
    """
    s = '\u2554' + 7 * '\u2550'
    s += (cols - 1) * ('\u2566' + 7 * '\u2550')
    s += '\u2557'
    return s


# the mid frame (horizontal frame) is relatively static, only repeated col-times
def midFrame(cols):
    """
    the top frame is relatively static, only repeated col-times
    :param cols: number of coulombs
    :return: ASCII-string of the line
    """
    s = '\u2560' + 7 * '\u2550'
    s += (cols - 1) * ('\u256C' + 7 * '\u2550')
    s += '\u2563'
    return s


# the bottom frame is relatively static, only repeated col-times
def botFrame(cols):
    """
    the top frame is relatively static, only repeated col-times
    :param cols: number of coulombs
    :return: ASCII-string of the line
    """
    s = '\u255A' + 7 * '\u2550'
    s += (cols - 1) * ('\u2569' + 7 * '\u2550')
    s += '\u255D'
    return s
