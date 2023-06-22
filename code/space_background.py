import pygame
from settings import *
from random import randint

class Space_Background:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.stars = []
        for n in range(30):
            x = randint(0, OPTIONS["SCREEN_WIDTH"])
            y = randint(0, OPTIONS["SCREEN_HEIGHT"])
            r = randint(1, 2)
            v = randint(50, 200)
            self.stars.append([(x,y), r, v])

    def create_star(self):
        x = randint(0, OPTIONS["SCREEN_WIDTH"])
        r = randint(1, 2)
        v = randint(50, 200)
        self.stars.append([(x,0), r, v])

    def update(self, dt):
        for star in self.stars[::-1]:
            star[0] = (star[0][0], star[0][1] + star[2] * dt)
            if star[0][1] > OPTIONS["SCREEN_HEIGHT"]:
                self.stars.remove(star)
                self.create_star()

    def display(self, dt):
        self.update(dt)
        for star in self.stars:
            pygame.draw.circle(self.display_surface, "white", star[0], star[1])
