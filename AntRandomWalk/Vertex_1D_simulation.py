import numpy
import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt


class Ant1D:
    def __init__(self, world, loc):
        self.world = world
        self.loc = loc

    def next_step(self):
        new_loc = self.world.random_neighbor(self.loc)
        world.change_in_vertices.append((new_loc, 1))
        self.loc = new_loc


class World1D:
    change_in_vertices = []

    def __init__(self, size):
        self.vertices = numpy.ones(size, int)
        self.size = size

    def random_neighbor(self, loc):
        left = self.vertices[loc - 1]
        right = self.vertices[loc + 1]
        r = random.uniform(0, 1)
        if r < left / (left + right):
            return (loc - 1) % self.size
        return (loc + 1) % self.size

    def update_vertices(self):
        for c in self.change_in_vertices:
            self.vertices[c[0]] += c[1]
        self.change_in_vertices = []


world = World1D(30)
ants = []
for index in range(4):
    ants.append(Ant1D(world, 15))
fig = plt.figure()


def animate(k):
    for ant in ants:
        ant.next_step()
    world.update_vertices()
    if k % 99 == 0:
        plt.cla()
        plt.yscale('log')
        plt.stem(range(30), world.vertices)
        for ant in ants:
            plt.plot(ant.loc, 1, '*')


ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
