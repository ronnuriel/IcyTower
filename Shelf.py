import random

import pygame

from Const import (HEIGHT, LEFT_WALL_BOUND, RIGHT_WALL_BOUND)
class Shelf:
    width_range = (4, 7)  # This will get overwritten based on difficulty

    def __init__(self, number):
        self.number = number
        self.width = random.randint(*self.width_range) * 32
        self.x = random.randint(LEFT_WALL_BOUND, RIGHT_WALL_BOUND - self.width)
        self.y = -number * 130 + HEIGHT - 25
        self.rect = pygame.Rect(self.x, self.y, self.width, 32)