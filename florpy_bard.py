import pygame
import numpy as np
import global_var as gv
from bard import Bard
from pipa import Pipa
from algo_gen import AlgoGen

class FlorpyBard:

    def __init__(self):
        # DIPLAY INFO
        self.w = gv.world_size_x
        self.h = gv.world_size_y
        self.bgcolor = (0xf1, 0xf2, 0xf3)
        self.fgcolor = (0, 0, 0)
        self.greencolor = (0, 0xff, 0)
        self.redcolor = (0xff, 0, 0)
        self.bluecolor = (0, 0, 0xff)

        self.delay = 0
        self.key_delay = 20
        self.key_interval = 60
        self.screen = pygame.display.set_mode((self.w + 1, self.h + 1))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        pygame.key.set_repeat(self.key_delay, self.key_interval)
        self.myfont = pygame.font.SysFont('Arial', 20)
        self.bard_example = None
        self.population_size = 15
        self.pipas = []
        self.algo_gen = AlgoGen(self.screen, self.population_size, 30, 50)
        self.count_active_car = 0
        self.gen = 0
        self.need_blocs_generation = True
        self.score = 0

    def main_loop(self):
        running = True
        clock = pygame.time.Clock()
        compute = True
        tmp = self.algo_gen.count_active_population()

        while running:
            clock.tick(90)
            if self.need_blocs_generation:
                self.add_pipas()
            if compute:
                self.count_active_car = self.algo_gen.count_active_population()
                if self.count_active_car > 0:
                    self.score += 1
                    if self.count_active_car != tmp:
                        print(f'Car count: {self.count_active_car}')
                        tmp = self.count_active_car
                    self.algo_gen.move_population()
                else:
                    # self.save_surface_to_image()
                    self.score = 0
                    self.gen += 1
                    print('no moving car anymore...')
                    self.algo_gen.the_circle_of_life()
                    for p in self.algo_gen.population:
                        p.reset_values()
                    self.need_blocs_generation = True
                    self.pipas = []
                    tmp = self.algo_gen.count_active_population()
                    pygame.time.delay(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    print(f'event.type={event.type}')
                    print(f'event.key={event.key}')
                    if event.key == pygame.K_q:
                        running = False
                    # if event.key == pygame.K_SPACE:
                    #     [x.jump() for x in self.bards]
                    if event.key == pygame.K_s:
                        compute = not compute
            self.draw_all()

    def draw_all(self):
        self.screen.fill(self.bgcolor)
        [x.draw() for x in self.algo_gen.population]
        [x.draw() for x in self.pipas]
        self.draw_text_info()
        pygame.display.flip()

    def draw_text_info(self):
        textsurface = self.myfont.render( f'Gen : {self.gen} | Score {self.score}', True, self.fgcolor)
        self.screen.blit(textsurface, (150, 25))

    def add_pipas(self):
        if len(self.pipas) == 0:
            p = Pipa(self.screen, 0)
            self.pipas.append(p)
            [x.add_pipa(p) for x in self.algo_gen.population]
        for p in self.pipas:
            if p.index == 0 and len(self.pipas) == 1 and p.pos_x < gv.world_size_x - (175 * 2):
                p = Pipa(self.screen, 1)
                self.pipas.append(p)
                [x.add_pipa(p) for x in self.algo_gen.population]
            if p.index == 0 and p.pos_x < gv.world_size_x - (175 * 4):
                p = Pipa(self.screen, 2)
                self.pipas.append(p)
                [x.add_pipa(p) for x in self.algo_gen.population]
                self.need_blocs_generation = False


if __name__ == '__main__':
    florpyBard = FlorpyBard()
    florpyBard.main_loop()
