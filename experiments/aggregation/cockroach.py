from experiments.aggregation.config import config
from simulation.agent import Agent
from simulation.utils import *


class Cockroach(Agent):
    def __init__(
            self, pos, v, aggregation, index: int, image: str = "experiments/aggregation/images/ant.png"
    ) -> None:
        super(Cockroach, self).__init__(
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

        self.aggregation = aggregation

    """ """
    def update_actions(self) -> None:
        # avoid any obstacles in the environment
        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        '''align_force, cohesion_force, separate_force = self.neighbor_forces()

        # combine the vectors in one
        steering_force = (
                align_force * config["boid"]["alignment_weight"]
                + cohesion_force * config["boid"]["cohesion_weight"]
                + separate_force * config["boid"]["separation_weight"]
        )

        # adjust the direction of the boid
        self.steering += truncate(
            steering_force / self.mass, config["boid"]["max_force"]
        )'''

