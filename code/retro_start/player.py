import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, change_state, group):
        super().__init__(group)
        self.frames = import_folder("../assets/player_ship")
        self.pos = pygame.math.Vector2(pos)
        self.frame_index = 0
        self.animation_speed = 5
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.speed = 0
        self.change_state = change_state

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def move(self, dt):
        self.pos += self.speed * pygame.math.Vector2(0,-1) * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom < 0:
            self.change_state("space_chase")

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
