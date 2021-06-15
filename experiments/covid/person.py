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
            self, pos, v, population, index: int, image = None, color = (255,255,255),
    ) -> None:
        """
                Args:
                ----
                    pos:
                    v:
                    flock:
                    index (int):
                    image (str): Defaults to "experiments/flocking/images/normal-boid.png"
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
            index=index
        )
        self.state = self.initial_state()
        self.population = population
        self.timer = 0

    def initial_state(self):
        if np.random.random() < 0.1:
            self.image.fill((255,0,0))
            return('infected')
        else:
            return('susceptible')

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
        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        neighbors = self.population.find_neighbors(self, config["agent"]["radius_view"])
        if self.state == 'susceptible':
            for neighbor in neighbors:
                if neighbor.state == 'infected':
                    self.change_state('infected')

        if self.state == 'infected':
            if multivariate_normal.rvs(mean = 0.4, cov= 0.1) > 1.5:
                self.change_state('recovered')

        if self.state == 'recovered':
            pass



