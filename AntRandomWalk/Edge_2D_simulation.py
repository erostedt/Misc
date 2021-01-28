import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as numpy


class Ant2D:
    def __init__(self, world, loc):
        self.world = world
        self.loc = loc

    def next_step(self):
        new_loc = self.world.random_neighbor(self.loc)
        world.moves.append(Move(self.loc, new_loc, 1))
        self.loc = new_loc


class Move:
    def __init__(self, old_loc, new_loc, n):
        self.old_loc = old_loc
        self.new_loc = new_loc
        self.n = n


class World2D:
    moves = []

    def __init__(self, size):
        self.size = size
        self.up = numpy.ones((size, size), int)
        self.right = numpy.ones((size, size), int)

    def random_neighbor(self, loc):
        left = self.right[loc[0] - 1, loc[1]]
        right = self.right[loc[0], loc[1]]
        down = self.up[loc[0], loc[1] - 1]
        up = self.up[loc[0], loc[1]]
        r = random.uniform(0, 1)
        tot = left + right + down + up
        if tot * r < left:
            return (loc[0] - 1) % self.size, loc[1]  # left
        if tot * r < left + right:
            return (loc[0] + 1) % self.size, loc[1]  # right
        if tot * r < left + right + down:
            return loc[0], (loc[1] - 1) % self.size  # down
        return loc[0], (loc[1] + 1) % self.size  # up

    def update_edges(self):
        for move in self.moves:
            dx = (move.new_loc[0] - move.old_loc[0]) % self.size
            dy = (move.new_loc[1] - move.old_loc[1]) % self.size
            if dx == 1:
                self.right[move.old_loc] += move.n
            elif dx > 1:
                self.right[move.new_loc] += move.n
            elif dy == 1:
                self.up[move.old_loc] += move.n
            else:
                self.up[move.new_loc] += move.n
        self.moves = []


def rotate_array(array, angle, wide=False):
    '''
    Rotates a rectangular or diamond 2D array in increments of 45 degrees.
    Parameters:
        array (list): a list containing sliceable sequences, such as list, tuple, or str
        angle (int): a positive angle for rotation, in 45-degree increments.
        wide (bool): whether a passed diamond array should rotate into a wide array
            instead of a tall one (tall is the default). No effect on square matrices.
    '''
    angle = angle%360
    if angle < 1:
        return [list(row) for row in array]
    lengths = list(map(len, array))
    rect = len(set(lengths)) == 1
    width = max(lengths)
    height = sum(lengths)/width
    if wide:
        width, height = height, width
    if not rect:
        array = [list(row) for row in array]
        array = [[array[row+col].pop() for row in range(width)] for col in range(height)]
        angle += 45
    nineties, more = divmod(angle, 90)
    if nineties == 3:
        array = list(zip(*array))[::-1]
    else:
        for i in range(nineties):
            array = list(zip(*array[::-1]))
    if more:
        ab = abs(len(array)-len(array[0]))
        m = min(len(array), len(array[0]))
        tall = len(array) > len(array[0])
        array = [[array[r][c] for r,c in zip(range(row-1, -1, -1), range(row))
                 ] for row in range(1, m+1)
           ] + [[array[r][c] for r,c in zip(range(m-1+row*tall, row*tall-1, -1),
                                            range(row*(not tall), m+row*(not tall)+1))
                ] for row in range(1, ab+(not tall))
           ] + [[array[r][c] for r,c in zip(range(len(array)-1, ab*tall+row-1, -1),
                                            range(ab*(not tall)+row, len(array[0])+(not tall)))
                ] for row in range((not tall), m)
           ]
    return array


world = World2D(9)
fig = plt.figure()
ants = []

for index in range(4):
    ants.append(Ant2D(world, (4, 4)))


def animate(k):
    for ant in ants:
        ant.next_step()
    world.update_edges()

    new_world = [[0 for x in range(2*world.size)] for y in range(2*world.size)]
    up_rotated = rotate_array(world.up,45)
    up_rotated.append([0])
    right_rotated = rotate_array(world.right,45)
    for row in range(int(len(new_world)/2)):
        current_vector = up_rotated[row]
        for numbers_in_vector in range(len(current_vector)):
                new_world[row][int(len(new_world)/2 - 1 - row + 2*numbers_in_vector)] = current_vector[numbers_in_vector]

        if row != 0:
            current_vector = right_rotated[row - 1]
            for numbers_in_vector in range(len(current_vector)):
                new_world[row][int(len(new_world)/2 - row + 2*numbers_in_vector)] = current_vector[numbers_in_vector]
    #Undre halvan, glöm inte "vända på ordningen"! (höger sen upp)
    for row in range(int(len(new_world)/2)):
        current_vector = right_rotated[int(row + len(new_world)/2) - 1]
#    print(current_vector)
        for numbers_in_vector in range(len(current_vector)):
            new_world[int(row + len(new_world)/2)][int(row + 2*numbers_in_vector)] = current_vector[numbers_in_vector]
        if row != int(len(new_world)/2 - 1):
            current_vector = up_rotated[int(row + len(new_world)/2)]
        else:
            current_vector = [0]
        for numbers_in_vector in range(len(current_vector)):
            new_world[int(row + len(new_world)/2)][int(row + 1 + 2*numbers_in_vector)] = current_vector[numbers_in_vector]
    if k % 9 == 0:
        matrix = numpy.vstack(new_world)
        temp = numpy.log(matrix)
        plt.cla()
        plt.imshow(temp)
        for r in range(len(matrix)):
            for c in range(len(matrix)):
                plt.text(c, r, matrix[r, c], horizontalalignment='center', fontsize='8')


ani = animation.FuncAnimation(fig, animate, interval='1')
plt.show()
