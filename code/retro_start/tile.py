import pygame
from timer import Timer

class Tile:
    def __init__(self, block_index, blocks, OPTIONS):
        self.OPTIONS = OPTIONS
        self.block_index = block_index
        self.rotation = 0
        self.tile_size = OPTIONS["RETRO_BLOCK_SIZE"]

        self.position = [5, 22]
        self.block_unit = blocks[self.block_index]

        self.move_timer = Timer(0.5, continuous = True)
        self.valid = True

        match self.block_index:
            case 0:
                self.blocks = [(-1,-1), (0,-1), (1,-1), (0,0), (0,1)]
            case 1:
                self.blocks = [(-1,-1), (0,-1), (1,-1), (-1,0), (-1,1)]
            case 2:
                self.blocks = [(0,-1), (0,0), (0,1)]
            case 3:
                self.blocks = [(1,-1), (1,0), (0,-1), (1,1)]
            case 4:
                self.blocks = [(-1,-1), (-1,0), (-1,1), (0,1)]
            case 5:
                self.blocks = [(-1,-1), (0,-1), (-1,0), (0,0)]

    def check_initial_placement(self, grid):
        for block in self.blocks:
            position = self.position.copy()
            position[0] += block[0]
            position[1] += block[1]
            if grid[position[1]][position[0]] != "":
                return False
        return True

    def move(self, grid, direction):
        #print(self.position)
        for block in self.blocks:
            position = self.position.copy()
            position[0] += direction[0] + block[0]
            position[1] += direction[1] + block[1]
            if position[0] < 0 or position[0] > self.OPTIONS["RETRO_SIZE"][0] - 1 or position[1] < 0 or grid[position[1]][position[0]] != "":
                if direction == (0, -1):
                    return True
                else:
                    return False

        self.position[0] += direction[0]
        self.position[1] += direction[1]

    def rotate(self, grid, direction):
        if not self.block_index == 5:
            new_blocks = []
            if direction == -1:
                for block in self.blocks:
                    temp = [0,0]
                    temp[0] = block[1]
                    temp[1] = block[0] * -1
                    new_blocks.append(temp)

            if direction == 1:
                for block in self.blocks:
                    temp = [0,0]
                    temp[0] = block[1] * -1
                    temp[1] = block[0]
                    new_blocks.append(temp)

            for block in new_blocks:
                position = self.position.copy()
                position[0] += block[0]
                position[1] += block[1]
                if position[0] < 0 or position[0] > self.OPTIONS["RETRO_SIZE"][0] - 1 or position[1] < 0 or grid[position[1]][position[0]] != "":
                    return

        self.blocks = new_blocks


    def update(self, grid, events, dt):
        placed = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    while not placed:
                        placed = self.move(grid, (0,-1))

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move(grid, (-1,0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move(grid, (1,0))

                elif event.key == pygame.K_q:
                    self.rotate(grid, -1)
                elif event.key == pygame.K_e:
                    self.rotate(grid, 1)

        if self.move_timer.update(dt) and not placed:
            placed = self.move(grid, (0,-1))

        if placed:
            self.place_block(grid)
            return True

    def place_block(self, grid):
        for block in self.blocks:
            position = self.position.copy()
            position[0] += block[0]
            position[1] += block[1]
            grid[position[1]][position[0]] = self.block_index


    def draw(self, grid_rect, surface):
        for block in self.blocks:
            position = self.position.copy()
            position[0] += block[0]
            position[1] += block[1]
            surface.blit(self.block_unit, (position[0]*self.tile_size + 1, (self.OPTIONS["RETRO_SIZE"][1]-6-position[1]) * self.tile_size + 1))
