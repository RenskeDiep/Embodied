from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm


class Aggregations(Swarm):
    """ """
    def __init__(self, screen) -> None:
        super(Aggregations, self).__init__(screen)

    def initialize(self, num_agents: int) -> None:
        if config["aggregation"]["obstacles"]:
            object1_loc = config["aggregation"]["object1_location"]
            object2_loc = config["aggregation"]["object2_location"]

            scale = [100, 100]

            filename = ("experiments/aggregation/images/greyc1.png")
            self.objects.add_object(file=filename, pos=object1_loc, scale=scale, obj_type="obstacle")

            filename = ("experiments/aggregation/images/greyc2.png")
            self.objects.add_object(file=filename, pos=object2_loc, scale=scale, obj_type="obstacle")

        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            self.add_agent(Cockroach(pos=np.array(coordinates), v=None, aggregation=self, index=index))
