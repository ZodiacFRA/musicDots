import math

import pygame


class Wall(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.center = (p1 + p2) / 2

        self.center_p1 = (self.center - self.p1).normalize()
        self.center_p2 = (self.center - self.p2).normalize()

        self.normal = (self.p2 - self.p1).rotate(-1 * math.pi / 2).normalize()

        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.line(
            screen, self.color, self.p1.to_int_tuple(), self.p2.to_int_tuple(), 2
        )
