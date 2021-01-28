import matplotlib.animation as animation
import numpy
import random
import matplotlib.pyplot as plt


class AdventurousAnt2D:
    def __init__(self, world, loc):
        self.world = world
        self.loc = loc
        self.old_loc = None

    def next_step(self):
        new_loc = self.world.random_neighbor(self.loc, self.old_loc)
        world.moves.append(Move(self.loc, new_loc, 1))
        self.old_loc = self.loc
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

    def random_neighbor(self, loc, old_loc):
        options = []
        options.append(((loc[0] - 1) % self.size, loc[1]))
        options.append(((loc[0] + 1) % self.size, loc[1]))
        options.append((loc[0], (loc[1] - 1) % self.size))
        options.append((loc[0], (loc[1] + 1) % self.size))
        for option in options:
            if option == old_loc:
                options.remove(option)

        r = random.uniform(0, 1)
        tot = 0
        for option in options:
            tot += self.vertices[option]

        s = 0
        for option in options:
            s += self.vertices[option]
            if s > tot * r:
                return option

    def update_vertices(self):
        for move in self.moves:
            self.vertices[move.new_loc] += move.n
        self.moves = []


size = 20
world = World2D(size)
fig = plt.figure()
ant = AdventurousAnt2D(world, (10, 10))

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
ani.save('one_ant_2D_adv.mp4', writer=writer)
