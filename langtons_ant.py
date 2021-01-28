import numpy as np
import matplotlib.pyplot as plt
##########################
# dir = {1 = up, 2 = right, 3 = down, 4 = left}


class Ant:
    def __init__(self, size, x, y, direction):
        self.board = np.zeros((size, size), int)
        self.x = x
        self.y = y
        self.direction = direction

    def update(self, x, y):
        if self.board[x][y] == 0:
            self.board[x][y] = 1
            self.direction += 1
            ant.fix_dir()
        else:
            self.board[x][y] = 0
            self.direction -= 1
            ant.fix_dir()
        ant.move()

    def move(self):
        if self.direction == 1:
            self.y += 1
        elif self.direction == 2:
            self.x += 1
        elif self.direction == 3:
            self.y -= 1
        else:
            self.x -= 1

    def fix_dir(self):
        if self.direction == 5:
            self.direction = 1
        elif self.direction == 0:
            self.direction = 4


ant = Ant(500, 250, 250, 1)

for i in range(20000):
    ant.update(ant.x, ant.y)

plt.imshow(ant.board)
plt.show()


