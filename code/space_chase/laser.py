import pygame
from timer import Timer
from pygame.math import Vector2 as vector

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, group, shooter = "enemy"):
        super().__init__(group)
        self.pos = pygame.math.Vector2(pos)

        self.switch_timer = Timer(0.2, continuous = True)
        self.switch_timer.activate()
        self.shooter = shooter
        if self.shooter == "enemy":
            self.image = pygame.image.load("../assets/particles/laser_bigger.png").convert_alpha()
            self.speed = 800
        else:
            self.image = pygame.image.load("../assets/particles/laser_player.png").convert_alpha()
            self.speed = -800

        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, enemy_group, player, dt):
        self.pos.y += self.speed * dt
        self.rect.centery = round(self.pos.y)

        if self.switch_timer.update(dt):
            self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)

        if self.shooter == "enemy":
            if self.rect.colliderect(player.sprite.rect):
                if self.mask.overlap(player.sprite.mask, vector(player.sprite.rect.topleft) - vector(self.rect.topleft)):
                    if not player.sprite.invincibility_timer.active:
                        player.sprite.take_damage(1)
                    self.kill()

        elif self.shooter == "player":
            for enemy in enemy_group.sprites():
                if self.rect.colliderect(enemy.rect):
                    if self.mask.overlap(enemy.mask, vector(enemy.rect.topleft) - vector(self.rect.topleft)):
                        enemy.take_damage(1)
                        self.kill()
