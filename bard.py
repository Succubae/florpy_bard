import pygame
import global_var as gv
import numpy as np

input_layer_size = 4
first_hidden_layer_size = 5
second_hidden_layer_size = 4
num_label = 2


class Bard:

    def __init__(self, surface):
        self.pos_x = gv.world_size_x / 2
        self.pos_y = gv.world_size_y / 2
        self.v_velocity = 0.0
        self.color = (0xff, 0, 0)
        self.size = 20
        self.surface = surface
        self.fitness_value = -1
        self.pipas = []
        self.active = True
        self.v_upper_distance = 0
        self.v_lower_distance = 0

        # ###### #
        # THETAS #
        # ###### #
        self.theta_1 = 2 * np.random.random_sample((first_hidden_layer_size, input_layer_size + 1)) - 1
        self.theta_2 = 2 * np.random.random_sample((second_hidden_layer_size, first_hidden_layer_size + 1)) - 1
        self.theta_3 = 2 * np.random.random_sample((num_label, second_hidden_layer_size + 1)) - 1
        self.all_thetas = [self.theta_1, self.theta_2, self.theta_3]

    def clone(self):
        clone = Bard(self.surface)
        for ts in range(len(self.all_thetas)):
            for ti in range(len(self.all_thetas[ts])):
                for tj in range(len(self.all_thetas[ts][ti])):
                    clone.all_thetas[ts][ti][tj] = self.all_thetas[ts][ti][tj]
        clone.fitness_value = self.fitness_value
        clone.pipas = self.pipas
        return clone

    def reset_values(self):
        self.pos_x = gv.world_size_x / 2
        self.pos_y = gv.world_size_y / 2
        self.v_velocity = 0.0
        self.fitness_value = -1
        self.color = (0xff, 0, 0)
        self.active = True
        self.pipas = []

    def get_sensors_value(self):
        return [self.pos_y, self.v_velocity, self.v_upper_distance, self.v_lower_distance]

    def order(self, best_move):
        if best_move == 1:
            self.jump()
            # print('JUMP !')

    def add_pipa(self, pipa):
        self.pipas.append(pipa)

    def apply_gravity(self):
        self.v_velocity += 0.4

    def check_world_collision(self):
        if self.pos_y < 0 or self.pos_y > gv.world_size_y:
            self.active = False
            self.color = (0, 0, 0xff)
            self.pos_x = 0 + self.size
            self.pos_y = 0 + self.size
            print('I\'m dead from the world...')

    def check_pipas_collision(self):
        for p in self.pipas:
            if p.pos_x < self.pos_x < p.pos_x + p.width \
                    and not p.upper_height < self.pos_y < p.upper_height + p.hole_size:
                self.active = False
                self.color = (0, 0, 0xff)
                self.pos_x = 0 + self.size
                self.pos_y = 0 + self.size
                print('I\'m dead from the pipe...')

    def get_closer_upper_lower_pipa_distance(self):
        v_distance = 0
        closer_pipa = {}
        for p in self.pipas:
            if p.pos_x + p.width < self.pos_x:
                continue
            closer_pipa[p] = p.pos_x - self.pos_x
        selected_pipa = None
        h_distance = gv.world_size_x
        for cp in closer_pipa.items():
            if cp[1] < h_distance:
                selected_pipa = cp[0]
                h_distance = cp[1]
        self.v_upper_distance = self.pos_y - selected_pipa.upper_height
        self.v_lower_distance = selected_pipa.upper_height + selected_pipa.hole_size - self.pos_y

    def move(self):
        self.get_closer_upper_lower_pipa_distance()
        if not self.active:
            self.pos_x = 0 + self.size / 2
            self.pos_y = 0 + self.size / 2
            return
        self.fitness_value += 1
        self.apply_gravity()
        self.pos_y += self.v_velocity
        self.check_world_collision()
        self.check_pipas_collision()

    def jump(self):
        # self.pos_y -= 75.
        self.v_velocity = -10.0

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.pos_x), int(self.pos_y)), int(self.size))
