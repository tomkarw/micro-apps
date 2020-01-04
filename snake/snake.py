import math
import random
import time

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

SNAKE_LEN = 3

DIRECTIONS = {
    UP: (0, 1),
    RIGHT: (1, 0),
    DOWN: (0, -1),
    LEFT: (-1, 0)
}


class Snake:
    def __init__(self, width, height, speed=1):

        self.width = width
        self.height = height

        self.body = []
        self.speed = speed
        self.direction = RIGHT

        random.seed(time.time())

        self.create()

        self.food = None
        self.place_food()

    @property
    def head(self):
        return self.body[0]

    def create(self):
        x, y = self.width//2, self.height//2
        for i in range(SNAKE_LEN):
            self.body.append(((x-i) % self.width, y))

    def place_food(self):
        x = random.getrandbits(int(math.log(self.width, 2)))
        y = random.getrandbits(int(math.log(self.height, 2)))
        while (x, y) in self.body:
            x = random.getrandbits(int(math.log(self.width, 2)))
            y = random.getrandbits(int(math.log(self.height, 2)))
        self.food = x, y

    def turn_right(self):
        self.direction = (self.direction - 1) % 4

    def turn_left(self):
        self.direction = (self.direction + 1) % 4

    def move(self, ate=False):
        if not ate:
            self.body.pop()
        x = (self.head[0] + DIRECTIONS[self.direction][0]) % self.width
        y = (self.head[1] + DIRECTIONS[self.direction][1]) % self.height
        self.body.insert(0, (x, y))

    def has_collided(self):
        return self.head in self.body[1:]

    def ate(self):
        ate = self.head == self.food
        if ate:
            self.place_food()
        return ate
