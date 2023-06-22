import pygame, sys
from time import perf_counter
from settings import *
from retro_start.map import *
from debug import debug
from space_background import Space_Background
from space_chase.space_level import Space_Level

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((OPTIONS["SCREEN_WIDTH"], OPTIONS["SCREEN_HEIGHT"]))
        pygame.display.set_caption("Retro's Revenge")
        self.state = "retro"


        self.retro = Map(OPTIONS, self.change_state)
        self.space_chase = Space_Level(self.change_state)
        self.background_manager = Space_Background()
        self.last_time = perf_counter()

        self.change_state("space_chase")


    def change_state(self, new_state):
        self.state = new_state

        if new_state == "space_chase":
            self.space_chase.start_timer.activate()

    def run(self):
        while True:
            current_time = perf_counter()
            dt = min(current_time - self.last_time, 0.1)
            self.last_time = current_time

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill("black")

            if self.state in ["retro", "space_chase"]:
                self.background_manager.display(dt)

            if self.state == "retro":
                self.retro.update(events, dt)
                self.retro.draw()

            if self.state == "space_chase":
                self.space_chase.update(events, dt)
                self.space_chase.draw()

            if self.state == "done":
                self.retro.draw()
            debug(round(1/dt))
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
