import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *
import numpy as np
from scipy.stats import multivariate_normal


class Virus(Agent):
    """ """
    def __init__(
            self, pos, v, population, index: int, image = None, color = (255,0,255),
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
        super(Virus, self).__init__(
            pos,
            v,
            image,
            color,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=2,
            height=2,
            dT=config["agent"]["dt"],
            index=index,
        )
        self.state = 'infecting'
        self.population = population
        self.avoided_obstacles: bool = False
        self.prev_pos = None
        self.prev_v = None
        self.timer = 0


    def change_state(self, state):
        self.state = state
        if state == 'non-infecting':
            self.image.fill((0,255,255,1))
        if state == 'infecting':
            self.image.fill((255,0,255))
            print('TEST')

    def update_actions(self) -> None:

        if self.state == 'infecting':
            self.timer += 1
            if self.timer >= 200:  #random getal
                self.change_state('non-infecting')

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
