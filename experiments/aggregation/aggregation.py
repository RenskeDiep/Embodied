from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm


class Aggregations(Swarm):
    """ """
    def __init__(self, screen) -> None:
        super(Aggregations, self).__init__(screen)

    def initialize(self, num_agents) -> None:

        # add obstacle/-s to the environment if present
        if config["base"]["site"]:
            object1_loc = config["objects"]["object1_location"]
            object2_loc = config["objects"]["object2_location"]

            scale1 = config["objects"]["object1_size"]
            scale2 = config["objects"]["object2_size"]

            filename = (
                "experiments/aggregation/images/greyc1.png"
                if config["base"]["background_grey"]
                else "experiments/aggregation/images/greyc2.png"
            )

            self.objects.add_object(
                file=filename, pos=object1_loc, scale=scale1, obj_type="site"
            )
            self.objects.add_object(
                file=filename, pos=object2_loc, scale=scale2, obj_type="site"
            )

            min_x, max_x = area(object1_loc[0], scale1[0])
            min_y, max_y = area(object1_loc[1], scale1[1])

