import pygame
from settings import *
from pygame.math import Vector2 as vector
from timer import Timer
from support import import_folder
from space_chase.laser import Laser
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, laser_group, group):
        super().__init__(group)
        self.pos = vector(OPTIONS["SCREEN_WIDTH"] // 2, OPTIONS["SCREEN_HEIGHT"] + 100)
        self.direction = vector(0,-1)
        self.laser_group = laser_group

        self.attack_timer = Timer(0.3)
        self.invincibility_timer = Timer(0.3)
        self.speed = 500

        self.frames = import_folder("../assets/player_ship")
        self.frame_index = 0
        self.animation_speed = 5
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.health = 3
        self.dead = False

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        if self.invincibility_timer.active:
            self.invincibility_timer.update(dt)
            if sin(self.invincibility_timer.time_elapsed * 70) < 0:
                self.image = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA)


    def input(self, events):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.direction.y = -1
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.direction.y = 1
        else:
            self.direction.y = 0

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.direction.x = -1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.direction.x = 1
        else:
            self.direction.x = 0

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if keys[pygame.K_SPACE] and not self.attack_timer.active:
            self.attack_timer.activate()
            Laser(self.rect.center, self.laser_group, "player")

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.dead = True
        else:
            self.invincibility_timer.activate()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos[0]), round(self.pos[1]))

        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx

        if self.rect.right > OPTIONS["SCREEN_WIDTH"]:
            self.rect.right = OPTIONS["SCREEN_WIDTH"]
            self.pos.x = self.rect.centerx

        if self.rect.bottom > OPTIONS["SCREEN_HEIGHT"]:
            self.rect.bottom = OPTIONS["SCREEN_HEIGHT"]
            self.pos.y = self.rect.centery



    def update(self, events, dt):
        if not self.dead:
            self.animate(dt)
            self.input(events)
            self.move(dt)
            self.attack_timer.update(dt)
