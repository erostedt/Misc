def donut_distance_1d(p1, p2, n):
        dx = (p1 - p2) % n
        return min(dx, n - dx)


def donut_distance_2d(p1, p2, n):
        dx = (p1[0]-p2[0]) % n
        dy = (p1[1]-p2[1]) % n
        return min(dx, n-dx) + min(dy, n-dy)
