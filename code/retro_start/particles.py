import pygame
from timer import Timer
from random import randint

class Particle(pygame.sprite.Sprite):
    def __init__(self, image, position, direction, group):
        super().__init__(group)
        self.pos = pygame.math.Vector2(position)
        self.direction = direction
        self.timer = Timer(2)
        self.timer.activate()
        self.original_speed = randint(10,40)
        self.speed = self.original_speed

        self.image = image
        self.rect = self.image.get_rect(center = self.pos)

    def update(self, dt):
        if self.timer.update(dt):
            self.kill()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        self.speed = max(self.original_speed - self.original_speed * self.timer.time_elapsed, 0)

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, group):
        super().__init__(group)
        self.original_image = pygame.image.load("../assets/particles/laser.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.original_image, direction.angle_to(pygame.math.Vector2(0,1)), 1)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.direction = direction
        self.speed = 1000

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
