import pygame
from pygame.math import Vector2 as vector
from space_chase.enemy import Enemy, Diving_Enemy
from timer import Timer

class Wave_Manager:
    def __init__(self, enemy_group, laser_group):
        self.enemy_group = enemy_group
        self.laser_group = laser_group
        self.current_wave = 1

        self.next_wave_timer = Timer(3)

        self.wave_info = {
        1:{
        "ships":[1,3,2,5,4,3,2,1],
        "locations":[vector(200,-100), vector(500,-150), vector(300,-200), vector(600,-50), vector(100,-100), vector(150,-100), vector(350,-100), vector(500,-100)],
        "type":"free"
        },

        2:{
        "ships":[0,0,0,0,0,0,0,0],
        "locations":[vector(200,-100), vector(500,-450), vector(300,-300), vector(600,-400), vector(100,-200), vector(150,-500), vector(350,-200), vector(500,-50)],
        "type":"diving"
        }

        }

        self.active_waves = []
        self.start_next_wave()

    def start_next_wave(self):
        self.current_wave += 1
        if not self.current_wave > len(self.wave_info):
            wave = Wave(self.wave_info[self.current_wave], self.enemy_group, self.laser_group)
            self.active_waves.append(wave)

    def update(self, dt):
        for wave in self.active_waves[::-1]:
            if not wave.wave_group.sprites():
                self.active_waves.remove(wave)
                self.next_wave_timer.activate()

        #print(self.next_wave_timer.time_elapsed)
        if self.next_wave_timer.update(dt):
            self.start_next_wave()
            print("check")


class Wave:
    def __init__(self, wave_info, enemy_group, laser_group):
        self.wave_info = wave_info
        self.wave_group = pygame.sprite.Group()
        self.enemy_group = enemy_group
        self.laser_group = laser_group
        if self.wave_info["type"] == "free":
            for index, enemy in enumerate(self.wave_info["ships"]):
                Enemy(self.wave_info["locations"][index], enemy, self.laser_group, [self.enemy_group, self.wave_group])
        else:
            for index, enemy in enumerate(self.wave_info["ships"]):
                Diving_Enemy(self.wave_info["locations"][index], enemy, [self.enemy_group, self.wave_group])
