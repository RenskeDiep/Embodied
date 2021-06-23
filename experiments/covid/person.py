import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *
import numpy as np
from scipy.stats import multivariate_normal


class Person(Agent):
    """ """
    def __init__(
            self, pos, v, population, index: int, age, image = None, color = (255,255,255),
    ) -> None:
        """
                Args:
                ----
                    pos:
                    v:
                    flock:
                    index (int):
                    image (str): Defaults to "experiments/flocking/images/normal-boid.png"
                    avoided_obstacles (bool):
                """
        super(Person, self).__init__(
            pos,
            v,
            image,
            color,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index,
        )
        self.age = age
        self.state = self.initial_state()
        self.population = population
        self.avoided_obstacles: bool = False
        self.prev_pos = None
        self.prev_v = None
        self.timer = 0
        self.sus_multiplier = self.susceptibility()

    def initial_state(self):
        if self.index < (config["base"]["n_agents"]/10):
            self.image.fill((255,0,0))
            return('infected')
        else:
            return('susceptible')

    def susceptibility(self):
        if self.age < 25:
            return 0.2
        elif self.age >= 25 and self.age <35:
            return 0.4
        elif self.age >= 35 and self.age < 45:
            return 0.8
        elif self.age >= 45 and self.age < 55:
            return 1.0
        elif self.age >= 55 and self.age < 65:
            return 1.3
        elif self.age >= 65:
            return 1.5
        else:
            return 1


    def change_state(self, state):
        self.state = state
        if state == 'susceptible':
            self.image.fill((255, 255, 255))
        if state == 'infected':
            self.image.fill((255,0,0))
            self.timer = 0
        if state == 'recovered':
            self.image.fill((0,255,0))

    def update_actions(self) -> None:

        particles = self.population.find_virus_particles(self, config["agent"]["radius_view"])
        neighbors = self.population.find_neighbors(self, config["agent"]["radius_view"])
        if self.state == 'recovered':
            self.population.datapoints.append('R')

        elif self.state == 'infected':
            self.population.datapoints.append('I')
            self.population.add_virus(self.pos)
            if multivariate_normal.rvs(mean=0.4, cov=0.1) > 1.35:  # random values, should be based on lit
                self.change_state('recovered')

        elif self.state == 'susceptible':
            self.population.datapoints.append('S')
            for particle in particles:
                if particle.state == 'infecting':
                    if self.sus_multiplier * multivariate_normal.rvs(mean=0.4, cov=0.1)  > 0.6:  # just random values, definitely need to be changed
                        self.change_state('infected')

        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                # If boid gets stuck because when avoiding the obstacle ended up inside of the object,
                # resets the position to the previous one and do a 180 degree turn back
                if not self.avoided_obstacles:
                    self.prev_pos = self.pos.copy()
                    self.prev_v = self.v.copy()

                else:
                    self.pos = self.prev_pos.copy()
                    self.v = self.prev_v.copy()

                self.avoided_obstacles = True
                self.avoid_obstacle()
                return

            self.prev_v = None
            self.prev_pos = None

            self.avoided_obstacles = False
