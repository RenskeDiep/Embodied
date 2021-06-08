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
            object_loc = config["base"]["object_location"]


            scale = [200, 200]

            filename = (
                "experiments/aggregation/images/greyc1.png"
                if config["base"]["background_grey"]
                else "experiments/aggregation/images/greyc2.png"
            )

            self.objects.add_object(
                file=filename, pos=object_loc, scale=scale, obj_type="site"
            )

            min_x, max_x = area(object_loc[0], scale[0])
            min_y, max_y = area(object_loc[1], scale[1])

