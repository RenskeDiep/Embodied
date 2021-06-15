import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *


class Person(Agent):
    """ """
    def __init__(
            self, pos, v, population, index: int, image: str = "experiments/flocking/images/normal-boid.png"
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
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index
        )
    def update_actions(self) -> None:
        pass

