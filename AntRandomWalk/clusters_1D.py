import numpy as np


def clusters(world):
    clusters = 0
    for point in range(np.size(world)):
        if world[point]:
            clusters += 1
            remove_neighbor_points(world, point)

    return clusters


def remove_neighbor_points(world, point):
    world[point] = False
    for point in neighbor_points(world, point):
        if world[point]:
            remove_neighbor_points(world, point)


def neighbor_points(world, point):
    if point == np.size(world) - 1:
        return [point - 1, 0]
    else:
        return [point - 1, point + 1]

