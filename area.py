import config, pygame
from random import sample, random

from config import State
from entity import Entity


class Area:
    def __init__(self,
                 simulation,
                 boundBox=((0, 0), (config.width, config.height)),
                 maskProbability=0, entityCount=0):

        self.simulation = simulation
        self.entityCount = 0
        self.boundBox = boundBox
        self.width = boundBox[1][0] - boundBox[0][0]
        self.height = boundBox[1][1] - boundBox[0][1]
        self.maskProbability = maskProbability
        self.entities = []
        self.image = pygame.Surface((self.width, self.height))
        self.boundThickness = 3

        self.fillEntities(entityCount)

    def fillEntities(self, entityCount=1):

        for i in range(entityCount):
            self.entities.append(Entity(homeArea=self,
                                        id=self.entityCount,
                                        hasMask=(random() <= self.maskProbability)))
            self.entityCount += 1



    def update(self):

        self.image.fill(config.colorBlack)

        pygame.draw.rect(self.image, config.colorWhite, pygame.Rect(0, 0, self.width, self.height), self.boundThickness)

        for entity in self.entities:
            entity.box = entity.box.move(entity.step)

        for entity in self.entities:
            entity.update()
            self.image.blit(entity.image, entity.box)


    def infectRandom(self, count=1):

        targets = []
        for entity in self.entities:
            if entity.state == State.SUSCEPTIBLE:
                targets.append(entity)

        for entity in sample(targets, min(len(targets), count)):
            entity.infect()
