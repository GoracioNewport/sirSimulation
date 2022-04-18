import config, pygame
from random import sample, random
from collections import Counter

from config import State
from entity import Entity


class areaBasic:
    def __init__(self, entityCount=100,
                 boundBox=((0, 0), (config.width, config.height)),
                 maskProbability=0,
                 quarantineMode=False,
                 quarantineBoxSize=50):

        self.entityCount = 0
        self.topLeftBound = boundBox[0]
        self.bottomRightBound = boundBox[1]
        self.width = boundBox[1][0] - boundBox[0][0]
        self.height = boundBox[1][1] - boundBox[0][1]
        self.maskProbability = maskProbability
        self.entities = []
        self.image = pygame.Surface((config.width, config.height))
        self.boundThickness = 3
        self.diseaseSpan = 0
        self.simulationOver = False

        self.fillEntities(entityCount)

    def fillEntities(self, entityCount = 1):

        for i in range(entityCount):
            self.entities.append(Entity(homeArea=self,
                                        id=self.entityCount,
                                        hasMask=(random() <= self.maskProbability)))
            self.entityCount += 1



    def update(self):

        pygame.draw.rect(self.image, config.colorWhite, pygame.Rect(0, 0, self.width, self.height), self.boundThickness)

        for entity in self.entities:
            entity.box = entity.box.move(entity.step)

        entityTypes = Counter()
        for entity in self.entities:
            entity.update()
            entityTypes[entity.state] += 1
            self.image.blit(entity.image, entity.box)

        if entityTypes[config.State.SUSCEPTIBLE] == 0:

            timeCut = 0
            for entity in self.entities:
                for event in entity.events:
                    if (event.type == config.EventType.DISEASE): timeCut = max(timeCut, event.timer)

            self.diseaseSpan += timeCut
            self.simulationOver = True

        elif entityTypes[config.State.INFECTIOUS]:
            self.diseaseSpan += 1
        elif entityTypes[config.State.INFECTIOUS] == 0:
            self.simulationOver = True



    def infectRandom(self, count = 1):

        targets = []
        for entity in self.entities:
            if entity.state == State.SUSCEPTIBLE:
                targets.append(entity)

        for entity in sample(targets, min(len(targets), count)):
            entity.infect()

    def reset(self):

        self.entities = [Entity(self, i, random() <= self.maskProbability) for i in range(self.entityCount)]
        self.diseaseSpan = 0
        self.simulationOver = False
        # self.infectRandom()