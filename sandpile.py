import numpy as np


def check_if_done(a, size, order):
    sum = 0
    for i in range(size):
        for j in range(size):
            if a[i][j] >= order:
                sum += 1
    return True if sum == 0 else False


#####################################
# Edges


def left(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i][j + 1] += 1
    c[i][j - 1] += 1
    c[i+1][j] += 1


def top(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i + 1][j] += 1
    c[i - 1][j] += 1
    c[i][j+1] += 1


def right(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i][j + 1] += 1
    c[i][j - 1] += 1
    c[i-1][j] += 1


def bottom(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i + 1][j] += 1
    c[i - 1][j] += 1
    c[i][j-1] += 1


############################################
# Corners
def lt(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i][j+1] += 1
    c[i+1][j] += 1


def rt(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i+1][j] += 1
    c[i][j-1] += 1


def rb(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i][j-1] += 1
    c[i-1][j] += 1


def lb(c, i, j, order):
    c[i][j] = c[i][j] - order
    c[i][j+1] += 1
    c[i-1][j] += 1


def spil(c, size, order):

    if not check_if_done(c, size, order):

        for i in range(size):
            for j in range(size):
                if c[i][j] >= order:
                    if i == 0 and j == 0:
                        lt(c, i, j, order)
                    elif i == 0 and j == size - 1:
                        rt(c, i, j, order)
                    elif i == size-1 and j == 0:
                        lb(c, i, j, order)
                    elif i == size-1 and j == size-1:
                        rb(c, i, j, order)
                    elif i == 0:
                        left(c, i, j, order)
                    elif i == size-1:
                        right(c, i, j, order)
                    elif j == 0:
                        top(c, i, j, order)
                    elif j == size-1:
                        bottom(c, i, j, order)
                    else:
                        c[i][j] = c[i][j] - order
                        c[i+1][j] += 1
                        c[i-1][j] += 1
                        c[i][j+1] += 1
                        c[i][j-1] += 1
        spil(c, size, order)


def print_sandpile(c, size):
    string = ''
    for i in range(size):
        for j in range(size):
            string += '|' + str(c[i][j]) + '| '
        print(string)
        if i < size-1:
            print('|---| |---| |---|')
        string = ''


def sandpile_addition(a, b, size, order):
    c = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            c[i][j] = a[i][j] + b[i][j]
    spil(c, size, order)
    print_sandpile(c, size)


############################
# run
size = 3
order = 4
a = 3*np.ones((3, 3))
b = np.zeros((3, 3))
b[1][1] = 1

sandpile_addition(a, b, size, order)
