import pygame
from pygame.image import load as load
from random import randint, random
from pygame.math import Vector2 as vector
import math
from settings import *
from timer import Timer
from space_chase.laser import Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, type, laser_group, group):
        super().__init__(group)
        self.image = load("../assets/retro_ships/" + str(type) + ".png").convert_alpha()
        self.laser_group = laser_group
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.desired_height = randint(50, 300)
        self.shoot_timer = Timer(0.5)
        self.shoot_chance = 0.25
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 400
        self.elapsed_time = random() * math.pi * 2

        self.health = 3


    def move(self, dt):
        self.elapsed_time += dt
        self.pos += vector(math.sin(self.elapsed_time) / 6, 1) * self.speed * dt
        if self.pos.y > self.desired_height: self.pos.y = self.desired_height
        if self.pos.x < 0 + 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]: self.pos.x = 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]
        if self.pos.x > OPTIONS["SCREEN_WIDTH"] - 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]: self.pos.x = OPTIONS["SCREEN_WIDTH"] - 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]

        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def shoot(self, dt):
        if not self.shoot_timer.active:
            if random() < self.shoot_chance * dt:
                Laser(self.rect.center, self.laser_group)
                self.shoot_timer.activate()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self, player, dt):
        self.move(dt)
        self.shoot(dt)
        self.shoot_timer.update(dt)

class Diving_Enemy(Enemy):
    def __init__(self, pos, type, group):
        super().__init__(pos, type, None, group)
        self.speed = 500

    def move(self, dt):
        self.elapsed_time += dt
        self.pos += vector(math.sin(self.elapsed_time * 5) / 10, 1) * self.speed * dt
        if self.pos.x < 0 + 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]: self.pos.x = 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]
        if self.pos.x > OPTIONS["SCREEN_WIDTH"] - 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]: self.pos.x = OPTIONS["SCREEN_WIDTH"] - 1.5 * OPTIONS["RETRO_BLOCK_SIZE"]

        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > OPTIONS["SCREEN_HEIGHT"]:
            self.rect.bottom = -5
            self.pos.y = self.rect.centery

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.mask.overlap(player.mask, vector(player.rect.topleft) - vector(self.rect.topleft)):
                player.take_damage(3)
                self.kill()

    def update(self, player, dt):
        self.move(dt)
        self.check_collision(player)
