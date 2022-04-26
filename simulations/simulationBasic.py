import config
from area import Area
from simulations.simulation import Simulation


class SimulationBasic(Simulation):
    def __init__(self,
                 boundBox=((0, 0), (config.width, config.height)),
                 maskProbability=0, quarantineMode=False,
                 entityCount=0, visualise=True):

        super().__init__(boundBox, maskProbability, quarantineMode, entityCount, visualise)
        self.areas.append(Area(self, entityCount=entityCount, maskProbability=maskProbability))

        self.initQuarantineZone()

    def reset(self):
        self.__init__(self.boundBox, self.maskProbability, self.quarantineMode, self.entityCount)