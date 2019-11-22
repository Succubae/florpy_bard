import operator
import random

import neural_network as nn

import color

import numpy as np
from bard import Bard

class AlgoGen:
    def __init__(self, pygame_surface, population_size, mutation_chance, mutation_rate):
        self.population = []
        for i in range(population_size):
            self.population.append(Bard(pygame_surface))
        self.population_size = population_size
        self.mutation_chance = mutation_chance
        self.mutation_rate = mutation_rate

    def get_ordered_population_by_fitness(self, to_print):
        val = {}
        for i in range(len(self.population)):
            val[self.population[i]] = self.population[i].fitness_value
        val = sorted(val.items(), key=operator.itemgetter(1), reverse=True)
        print([x[1] for x in val]) if to_print else ''
        return val

    # ########################################
    # SELECTION
    # ########################################
    def get_fitness_sum(self):
        fitness_sum = 0
        for p in self.population:
            fitness_sum += p.fitness_value
        return fitness_sum

    def select_based_on_fitness(self, fitness_sum):
        rand = np.random.random() * fitness_sum
        running_sum = 0
        for i in range(len(self.population)):
            running_sum += self.population[i].fitness_value
            if running_sum > rand:
                return self.population[i].clone()

    def breed_child(self, p1: Bard, p2: Bard):
        child = Bard(p1.surface)
        for ts in range(len(child.all_thetas)):
            for ti in range(len(child.all_thetas[ts])):
                for tj in range(len(child.all_thetas[ts][ti])):
                    child.all_thetas[ts][ti][tj] = p1.all_thetas[ts][ti][tj] if random.random() * 100 < 50 else p2.all_thetas[ts][ti][tj]
        return child

    def selection(self):
        select = [self.population[0].clone()]
        # THIS WOULD NEED A BIT OF DISTANCE-BASED SELECTION
        fitness_sum = self.get_fitness_sum()
        while True:
            if len(select) == self.population_size: break
            first_parent = self.select_based_on_fitness(fitness_sum)
            second_parent = self.select_based_on_fitness(fitness_sum)
            child = self.breed_child(first_parent, second_parent)
            if len(select) == self.population_size: break
            select.append(first_parent)
            if len(select) == self.population_size: break
            select.append(second_parent)
            if len(select) == self.population_size: break
            select.append(child)
        self.population = select

    # ########################################
    # CROSS BREED
    # ########################################
    def cross_breed(self):
        children = []
        print(f'to_breed: ({self.population_size - len(self.population)})' )
        for i in range(self.population_size - len(self.population)):
            children.append(self.breed_child(self.population[i % len(self.population)], self.population[abs(int(len(self.population) - i - 1)) % len(self.population)]))
        self.population.extend(children)
        return self.population

    # ########################################
    # MUTATION
    # ########################################
    def mutate(self, individual):
        mut = 0
        no_mut = 0
        for ts in range(len(individual.all_thetas)):
            for ti in range(len(individual.all_thetas[ts])):
                for tj in range(len(individual.all_thetas[ts][ti])):
                    if random.random() * 100 < self.mutation_rate:
                        mut += 1
                        individual.all_thetas[ts][ti][tj] += nn.get_random_value_within_boundaries()
                        individual.all_thetas[ts][ti][tj] = nn.limit_theta_value_to_boundaries(individual.all_thetas[ts][ti][tj])
                    else:
                        no_mut += 1
        print(f'MUTATED {mut} TIMES OVER {mut + no_mut}!')
        return individual

    def mutate_population(self):
        for i in range(len(self.population)):
            if i == 0:
                continue
            if random.random() * 100 < self.mutation_chance:
                self.population[i] = self.mutate(self.population[i])

    # ########################################
    # ACTION
    # ########################################
    @staticmethod
    def move_individual(individual):
        if individual.active:
            individual.move()
            best_move = nn.neural_network(individual.get_sensors_value(), individual.theta_1, individual.theta_2, individual.theta_3) + 1
            individual.order(best_move)

    def move_population(self):
        [self.move_individual(individual) for individual in self.population]
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(False)]

    # ########################################
    # THE CIRCLE OF LIIIIIIIFE
    # ########################################
    def the_circle_of_life(self):
        # print('Cycle')
        print(f'{color.OKBLUE}Population fitness before selection new generation{color.ENDC}')
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(True)]
        # ------------------------------------------------------------
        print(f'Population size for selection = {len(self.population)}')
        self.selection()
        # ------------------------------------------------------------
        print(f'Population size for cross_breed = {len(self.population)}')
        self.cross_breed()
        # ------------------------------------------------------------
        print(f'Population size for mutate_population = {len(self.population[1:])}')
        self.mutate_population()
        # ------------------------------------------------------------
        print(f'{color.OKBLUE}Population fitness after new generation{color.ENDC}')
        self.population = [x[0] for x in self.get_ordered_population_by_fitness(True)]
        print(f'Population size after cycle = {len(self.population)}')

    # ########################################
    # OTHER
    # ########################################
    def count_active_population(self):
        cnt = 0
        for c in self.population:
            if c.active:
                cnt += 1
        return cnt
