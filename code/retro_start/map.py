import pygame
from retro_start.tile import Tile
from support import import_folder
from random import randint, random, choice
from retro_start.particles import Particle, Laser
from pygame.image import load as load
from pygame.math import Vector2 as vector
import math
from timer import Timer
from retro_start.player import Player

class Map:
    def __init__(self, OPTIONS, change_state):
        self.display_surface = pygame.display.get_surface()
        self.OPTIONS = OPTIONS
        self.grid_width = OPTIONS["RETRO_SIZE"][0]
        self.grid_height = OPTIONS["RETRO_SIZE"][1]
        self.tile_size = OPTIONS["RETRO_BLOCK_SIZE"]
        self.grid = [["" for x in range(self.grid_width)] for y in range(self.grid_height)]
        self.change_state = change_state

        self.active = True
        self.completed = False
        self.exploded = False
        self.input1 = False
        self.start_fleeing = False
        self.flee_started = False


        self.particles = pygame.sprite.Group()
        self.particle_timer = Timer(2)
        self.particle_surfs = [load("../assets/particles/explosion_particle1.png").convert_alpha(), load("../assets/particles/explosion_particle2.png").convert_alpha()]
        self.preview_surfs = import_folder("../assets/retro_ships")
        self.font = pygame.font.Font("../assets/fonts/joystix monospace.otf", 40)
        self.text_font = pygame.font.Font("../assets/fonts/joystix monospace.otf", 30)

        self.flee_timer = Timer(1)

        for y in range(4):
            for x in range(self.grid_width):
                if random() < 0.5:
                    self.grid[y][x] = randint(0,5)

        self.grid_background = pygame.Surface((self.grid_width * self.tile_size, (self.grid_height - 5) * self.tile_size), pygame.SRCALPHA)
        self.grid_background.set_colorkey((0,0,0))
        self.grid_rect = self.grid_background.get_rect(center = (OPTIONS["SCREEN_WIDTH"]//2, OPTIONS["SCREEN_HEIGHT"]//2))

        self.player = pygame.sprite.GroupSingle()
        Player(vector(self.grid_rect.midleft) + vector(-130, -96), self.change_state, self.player)

        for x in range(0, self.grid_background.get_width(), self.tile_size):
            pygame.draw.line(self.grid_background, "white", (x, 0), (x, self.grid_background.get_height()), 1)

        for y in range(0, self.grid_background.get_height(), self.tile_size):
            pygame.draw.line(self.grid_background, "white", (0, y), (self.grid_background.get_width(), y), 1)

        self.next_surf = self.font.render("NEXT", False, "White")
        self.next_rect = self.next_surf.get_rect(midtop = (self.tile_size * 2.5 + self.grid_rect.right + 4, self.grid_rect.top))

        self.text_box_surf = load("../assets/text_boxes/retro_box.png")
        self.text_box_rect = self.text_box_surf.get_rect(center = (self.grid_rect.centerx - 30, self.grid_rect.centery - 90))

        self.text_surf1 = self.text_font.render("DID YOU JUST", False, "Black")
        self.text_rect1 = self.text_surf1.get_rect(midtop = self.text_box_rect.midtop + vector(-15, 25))

        self.text_surf2 = self.text_font.render("KILL THEM!!", False, "Black")
        self.text_rect2 = self.text_surf2.get_rect(midtop = self.text_box_rect.midtop + vector(-15, 65))

        self.text_surf3 = self.text_font.render("YOU WILL PAY", False, "Black")
        self.text_rect3 = self.text_surf3.get_rect(midbottom = self.text_box_rect.midbottom - vector(15, 80))

        self.text_surf4 = self.text_font.render("FOR THIS!!", False, "Black")
        self.text_rect4 = self.text_surf4.get_rect(midbottom = self.text_box_rect.midbottom - vector(15, 40))

        self.logo_surf = load("../assets/logo/retro_logo.png").convert_alpha()
        self.logo_surf = pygame.transform.rotozoom(self.logo_surf, 0, 0.7)
        self.logo_rect = self.logo_surf.get_rect(bottomleft = self.grid_rect.bottomright + vector(15, 0))

        self.block_surfs = import_folder("../assets/retro_pieces")
        self.active_tile = Tile(randint(0,5), self.block_surfs, OPTIONS)
        self.next_ships = [Tile(randint(0,5), self.block_surfs, OPTIONS) for x in range(3)]

    def check_lines(self):
        for y in range(self.grid_height):
            full_line = True
            for x in self.grid[y]:
                if x == "":
                    full_line = False
            if full_line:
                self.win_line = y
                self.win_line_content = self.grid[y].copy()

                return True

    def create_particles(self):
        start_pos_x = self.grid_rect.left + self.tile_size // 2
        start_pos_y = self.grid_rect.bottom - (self.win_line + 0.5) * self.tile_size
        start_pos = vector(start_pos_x, start_pos_y)
        self.particle_timer.activate()

        for x in range(self.grid_width):
            current_pos = start_pos + vector(self.tile_size * x,0)
            for r in range(40):
                degrees = randint(1,360)
                direction = vector(math.cos(math.radians(degrees)), math.sin(math.radians(degrees)))
                Particle(choice(self.particle_surfs), current_pos, direction, [self.particles])


    def update(self, events, dt):
        self.player.update(dt)
        self.particles.update(dt)

        if self.active:
            if self.active_tile.update(self.grid, events, dt):
                del self.active_tile
                if self.check_lines():
                    self.completed = True
                    self.active = False
                    self.create_particles()
                else:
                    self.active_tile = self.next_ships.pop(0)
                    self.next_ships.append(Tile(randint(0,5), self.block_surfs, self.OPTIONS))
                    if not self.active_tile.check_initial_placement(self.grid):
                        self.active = False

        if self.completed:
            if self.particle_timer.update(dt):
                for x in range(len(self.grid[self.win_line])):
                    self.grid[self.win_line][x] = ""
                self.exploded = True

        if self.exploded:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.input1:
                            self.start_fleeing = True
                        else:
                            self.input1 = True

        if self.flee_timer.update(dt):
            self.flee_started = True

        if self.flee_started:
            self.player.sprite.speed += 200 * dt

    def draw(self):
        background_copy = self.grid_background.copy()
        self.player.draw(self.display_surface)

        if self.active:
            self.active_tile.draw(self.grid_rect, background_copy)

        for x in range(self.grid_width):
            for y in range(self.grid_height - 5):
                if self.grid[y][x] != "":
                    background_copy.blit(self.block_surfs[self.grid[y][x]], (x*self.tile_size + 1, (self.grid_height-6-y) * self.tile_size + 1))

        self.display_surface.blit(background_copy, self.grid_rect)
        self.display_surface.blit(self.logo_surf, self.logo_rect)
        pygame.draw.rect(self.display_surface, "white", self.grid_rect, 2)

        self.display_surface.blit(self.next_surf, self.next_rect)

        for index, ship in enumerate(self.next_ships):
            x = self.tile_size * 2.5 + self.grid_rect.right
            y = self.tile_size * (4 + 3.5 * index) + self.grid_rect.top
            surf = self.preview_surfs[ship.block_index]
            rect = surf.get_rect(center = (x,y))
            self.display_surface.blit(surf, rect)

        if self.exploded:
            self.display_surface.blit(self.text_box_surf, self.text_box_rect)
            self.display_surface.blit(self.text_surf1, self.text_rect1)
            self.display_surface.blit(self.text_surf2, self.text_rect2)
            if self.input1:
                self.display_surface.blit(self.text_surf3, self.text_rect3)
                self.display_surface.blit(self.text_surf4, self.text_rect4)
                if self.start_fleeing:
                    self.exploded = False
                    self.flee_timer.activate()
                    for index, ship in enumerate(self.next_ships):
                        x = self.tile_size * 2.5 + self.grid_rect.right
                        y = self.tile_size * (4 + 3.5 * index) + self.grid_rect.top
                        direction = (self.player.sprite.pos + vector(0,choice([-50, 50])) - vector(x,y)).normalize()
                        Laser(vector(x,y), direction, self.particles)

        self.particles.draw(self.display_surface)
