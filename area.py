import config, pygame
from random import sample, random
from collections import Counter

from config import State
from entity import Entity


class Area:
    def __init__(self, entityCount, x1, y1, x2, y2, maskProbability):
        self.entityCount = entityCount
        self.topLeftBound = (x1, y1)
        self.bottomRightBound = (x2, y2)
        self.width = x2 - x1
        self.height = y2 - y1
        self.maskProbability = maskProbability
        self.entities = [Entity(self, i, random() <= 
            self.maskProbability) for i in range(self.entityCount)]
        self.image = pygame.Surface((config.width, config.height))
        self.boundThickness = 3
        self.diseaseSpan = 0
        self.simulationOver = False

        # self.infectRandom()

    def update(self):

        self.image.fill(config.colorBlack)
        pygame.draw.rect(self.image, config.colorWhite, 
            pygame.Rect(0, 0, self.width, self.height), 
            self.boundThickness)

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
        self.infectRandom()