from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)
        # To do

    def initialize(self, num_agents: int) -> None:
        """
        Args:
            num_agents (int):

        """
        if config["population"]["obstacles"]:
            object1_loc = config["population"]["object1_location"]
            scale1 = config["population"]["scale1"]
            filename = ("experiments/aggregation/images/greyc2.png")
            self.objects.add_object(file=filename, pos=object1_loc, scale=scale1, obj_type="obstacle")

        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            if config["population"]["obstacles"]:  # you need to define this variable
                for obj in self.objects.obstacles:
                    rel_coordinate = relative(
                        coordinates, (obj.rect[0], obj.rect[1])
                    )
                    try:
                        while obj.mask.get_at(rel_coordinate):
                            coordinates = generate_coordinates(self.screen)
                            rel_coordinate = relative(
                                coordinates, (obj.rect[0], obj.rect[1])
                            )
                    except IndexError:
                        pass
            self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index))
