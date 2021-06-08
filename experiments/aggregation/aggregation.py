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
            con_object_loc = config["aggregation"]["containing_object_location"]

            scale1 = config["aggregation"]["object1_scale"]
            scale2 = config["aggregation"]["object2_scale"]
            con_scale = config["aggregation"]["containing_object_scale"]

            # containing object
            filename = ("experiments/flocking/images/redd.png")
            self.objects.add_object(file=filename, pos=con_object_loc, scale=con_scale, obj_type="obstacle")

            filename = ("experiments/aggregation/images/greyc2.png")
            #site 1
            self.objects.add_object(file=filename, pos=object1_loc, scale=scale1, obj_type="site")
            #site 2
            self.objects.add_object(file=filename, pos=object2_loc, scale=scale2, obj_type="site")

            min_x, max_x = area(con_object_loc[0], con_scale[0])
            min_y, max_y = area(con_object_loc[1], con_scale[1])


        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            self.add_agent(Cockroach(pos=np.array(coordinates), v=None, aggregation=self, index=index))
