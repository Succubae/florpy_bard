import pygame
import numpy as np
import global_var as gv

upper_lower_bounds = 450

class Pipa:

    def __init__(self, surface, index):
        self.index = index
        self.pos_x = gv.world_size_x
        self.upper_height = 300
        self.hole_size = 250
        self.width = 100
        self.surface = surface
        self.color = (0, 0xff, 0)

    def draw(self):
        self.move()
        upper_rect = pygame.Rect(self.pos_x, 0, self.width, self.upper_height)
        lower_rect = pygame.Rect(self.pos_x, self.upper_height + self.hole_size, self.width, gv.world_size_y)
        pygame.draw.rect(self.surface, self.color, upper_rect)
        pygame.draw.rect(self.surface, self.color, lower_rect)

    def move(self):
        self.pos_x -= 6
        if self.pos_x < 0 - self.width:
            self.pos_x = gv.world_size_x
            self.upper_height = int(np.random.random() * gv.world_size_y)
            print(f'Upper height = {self.upper_height}')
            if self.upper_height < upper_lower_bounds:
                self.upper_height = upper_lower_bounds
            elif self.upper_height > gv.world_size_y - upper_lower_bounds:
                self.upper_height = gv.world_size_y - upper_lower_bounds
