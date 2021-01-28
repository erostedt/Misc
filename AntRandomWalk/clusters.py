import numpy as np
pos_vector = []


def clusters(a, nbrs, final_ant_pos):
    clusters = 0
    max_num = 0
    size = np.size(a, 0)
    cluster_centers = []
    for row in range(np.size(a, 0)):
        for col in range(np.size(a, 1)):
            if a[row][col]:
                clusters += 1
                max_positions(row, col, a, nbrs, max_num)
                cluster_center = pos_vector[-1]
                cluster_centers.append(cluster_center)

    ants_in_clusters = ants_in_cluster(final_ant_pos, cluster_centers, size)

    return clusters, cluster_centers, ants_in_clusters


def old_clusters(a, nbrs):
    clusters = 0
    max_num = 0
    cluster_centers = []
    for row in range(np.size(a, 0)):
        for col in range(np.size(a, 1)):
            if a[row][col]:
                clusters += 1
                max_positions(row, col, a, nbrs, max_num)
                cluster_center = pos_vector[-1]
                cluster_centers.append(cluster_center)

    return clusters, cluster_centers


def remove_neighbors(row, col, a):
    a[row][col] = False
    for r, c in neighbors(row, col, a):
        if a[r][c]:
            remove_neighbors(r, c, a)


def neighbors(row, col, a):
    rows = np.size(a, 0)
    cols = np.size(a, 1)
    return [(row, (col + 1) % cols), (row, (col-1) % cols), ((row + 1) % rows, col), ((row - 1) % rows, col)]


def max_positions(row, col, a, nbrs, max_num):
    if nbrs[row][col] > max_num:
        max_num = nbrs[row][col]
        pos = [row, col]
        pos_vector.append(pos)
    a[row][col] = False
    for r, c in neighbors(row, col, a):
        if a[r][c]:
            max_positions(r, c, a, nbrs, max_num)


def ave_dist(neighbors):
    distance_vector = []
    if np.size(neighbors) <= 1:
        return 0
    i = 1
    for pos in neighbors:
        for other_pos in neighbors[i:]:
            if pos != other_pos:
                ts = np.sqrt(((pos[0] - other_pos[0])**2 + (pos[1] - other_pos[1])**2))
                distance_vector.append(ts)
        i += 1
    return np.mean(distance_vector)


def ants_in_cluster(final_ant_pos, cluster_centers, size):
    ants_in_clust = []
    for cluster_center in cluster_centers:
        temp = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = cluster_center[0] + i
                y = cluster_center[1] + j

                if x == -1:
                    x = size - 1

                if x == size:
                    x = 0
                elif x == size + 1:
                    x = 1

                if y == -1:
                    y = size - 1

                if y == size:
                    y = 0
                elif y == size + 1:
                    y = 1

                for ant_pos in final_ant_pos:
                    if ant_pos[0] == x and ant_pos[1] == y:
                        temp += 1

        ants_in_clust.append(temp)

    return ants_in_clust
