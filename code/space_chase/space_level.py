import pygame
from settings import *
from space_chase.player import Player
from space_chase.wave_manager import Wave_Manager
from timer import Timer

class Space_Level:
    def __init__(self, change_state):
        self.display_surface = pygame.display.get_surface()
        self.map_width = OPTIONS["SCREEN_WIDTH"]
        self.map_height = OPTIONS["SCREEN_HEIGHT"]

        self.change_state = change_state

        self.start_timer = Timer(0.4)

        self.enemy_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        Player(self.laser_group, self.player)

        self.player_health_icon = pygame.transform.scale(self.player.sprite.image, (32,32))

        self.wave_manager = Wave_Manager(self.enemy_group, self.laser_group)

        self.started = False

    def draw_player_health(self):
        for life in range(self.player.sprite.health - 1):
            x = self.map_width - 15 - 48 * life
            y = self.map_height - 15
            rect = self.player_health_icon.get_rect(bottomright = (x,y))
            self.display_surface.blit(self.player_health_icon, rect)

    def draw(self):
        self.laser_group.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.enemy_group.draw(self.display_surface)

        self.draw_player_health()

    def update(self, events, dt):
        if not self.started:
            if self.start_timer.update(dt):
                self.started = True
                self.player.sprite.direction = pygame.math.Vector2(0,0)
                self.player.sprite.speed = 300
            self.player.sprite.move(dt)
            self.player.sprite.animate(dt)

        else:
            self.wave_manager.update(dt)
            if not self.player.sprite.dead:
                self.player.update(events, dt)
                self.enemy_group.update(self.player.sprite, dt)
                self.laser_group.update(self.enemy_group, self.player, dt)

            #print(self.laser_group)
