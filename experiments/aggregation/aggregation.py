from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm


class Aggregations(Swarm):
    """ """
    def __init__(
            self,screen,points_to_plot
    )-> None:
            super(Aggregations, self).__init__(
            screen,
            points_to_plot,
        )
