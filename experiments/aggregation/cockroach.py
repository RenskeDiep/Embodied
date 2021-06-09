from experiments.aggregation.config import config
from simulation.agent import Agent
from simulation.utils import *
from scipy.stats import multivariate_normal


class Cockroach(Agent):
    def __init__(
            self, pos, v, aggregation, index: int, image: str = "experiments/aggregation/images/ant.png", state = 'wandering', timer = 0
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
        self.state = state
        self.timer = timer

    def change_state(self, new_state):
        #possible states are 'wandering', 'joining', 'leaving' and 'still'
        self.state = new_state
        pass

    def find_neighbors(self, agent: Agent, radius: float) -> list:
        """
        Try to locate all the neighbors of the given agent, considering a specified radius, by computing the euclidean
        distance between the agent and any other member of the swarm

        Args:
        ----
            agent (Agent):
            radius (float):

        """
        #  Check that the each other agent is not our considered one, if the type is None or infected, and the distance
        return [neighbor for neighbor in self.agents if
                agent is not neighbor  and
                self.compute_distance(agent, neighbor) < radius]

    def site_behaviour(self):
        if self.state == 'wandering':
            """"probability function Pjoin to consider joining, dependent on neighbours in radius"""
            neighbors_in_radius = len(self.find_neighbors(self, config["agent"]["radius_view "]))
            neighbor_percentage = neighbors_in_radius / (config["base"]["n_agents"])
            Pjoin = multivariate_normal(mean=neighbor_percentage, cov=0.2)
            if Pjoin > 0.5:  # random value, idk...
                self.change_state('joining')
                self.timer = 0
        if self.state == 'still':
            """"probability function Pleave to consider leaving dependent on neighbours in radius"""
            neighbors_in_radius = len(self.find_neighbors(self, config["agent"]["radius_view "]))
            neighbor_percentage = neighbors_in_radius / (config["base"]["n_agents"])
            Pleave = multivariate_normal(mean= (1-neighbor_percentage), cov=0.2)
            if Pleave > 0.5:  # random value, idk...
                self.change_state('leaving')
                self.timer = 0
        pass

    def update_actions(self) -> None:
        # avoid any obstacles in the environment
        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()


        if self.state == 'wandering':
            # check if agent on aggregation site
            for site in self.aggregation.objects.sites:
                on_site = pygame.sprite.collide_mask(self, obstacle)
                if bool(on_site):
                    self.site_behaviour()

        if self.state == 'joining':
            self.timer += 1
            if self.timer > 10: #Tjoin, we should give this a value somewhere...
                self.change_state(('still'))

        if self.state == 'still':
            self.site_behaviour()

        if self.state == 'leaving':
            self.timer += 1
            if self.timer > 10: #Tleave, we should give this a value somewhere
                self.change_state('wandering')

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

