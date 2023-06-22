import pygame

class Timer:
    def __init__(self, duration, continuous = False):
        self.duration = duration
        self.continuous = continuous
        self.active = False
        self.time_elapsed = 0

        if self.continuous:
            self.activate()

    def activate(self, reset = True):
        self.active = True
        if reset:
            self.time_elapsed = 0

    def deactivate(self):
        self.active = False

    def update(self, dt):
        if self.active:
            self.time_elapsed += dt
            if self.time_elapsed >= self.duration:
                if self.continuous:
                    self.time_elapsed -= self.duration
                else:
                    self.deactivate()
                    self.time_elapsed = 0
                return True
            return False
