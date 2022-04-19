import config
from area import Area
from simulations.simulation import Simulation


class SimulationBasic(Simulation):
    def __init__(self,
                 boundBox=((0, 0), (config.width, config.height)),
                 maskProbability=0, quarantineMode=False,
                 entityCount=100):

        super().__init__(boundBox=boundBox, maskProbability=maskProbability, quarantineMode=quarantineMode)

        self.areas = [Area(entityCount=entityCount, maskProbability=maskProbability)]