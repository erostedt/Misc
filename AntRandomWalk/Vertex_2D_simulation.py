import numpy
import random
import matplotlib.pyplot as plt
import time as time
import matplotlib.animation as animation


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
        self.new_loc = new_loc
        self.n = n


class World2D:
    moves = []

    def __init__(self, size):
        self.size = size
        self.vertices = numpy.ones((size, size), int)

    def random_neighbor(self, loc):
        left = self.vertices[loc[0] - 1, loc[1]]
        right = self.vertices[(loc[0] + 1) % self.size, loc[1]]
        down = self.vertices[loc[0], loc[1] - 1]
        up = self.vertices[loc[0], (loc[1] + 1) % self.size]
        r = random.uniform(0, 1)
        tot = left + right + down + up
        if tot * r < left:
            return (loc[0] - 1) % self.size, loc[1]  # left
        if tot * r < left + right:
            return (loc[0] + 1) % self.size, loc[1]  # right
        if tot * r < left + right + down:
            return loc[0], (loc[1] - 1) % self.size  # down
        return loc[0], (loc[1] + 1) % self.size  # up

    def update_vertices(self):
        for move in self.moves:
            self.vertices[move.new_loc] += move.n
        self.moves = []


size = 20
world = World2D(size)
fig = plt.figure()
ant = Ant2D(world, (10, 10))

Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800)


def animate(k):
    ant.next_step()
    world.update_vertices()

    plt.cla()
    matrix = world.vertices
    temp = numpy.log(world.vertices)
    plt.imshow(temp)

    plt.plot(ant.loc[1], ant.loc[0], 'k*')

    for r in range(len(matrix)):
        for c in range(len(matrix)):
            plt.text(c, r, matrix[r, c], horizontalalignment='center', fontsize='6')


ani = animation.FuncAnimation(fig, animate, frames=3000, repeat=True)
ani.save('one_ant_2D.mp4', writer=writer)

