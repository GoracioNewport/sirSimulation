import config, pygame
from random import sample
from collections import Counter

from config import State
from entity import Entity


class Area:
    def __init__(self, entityCount, x1, y1, x2, y2):
        self.entityCount = entityCount
        self.topLeftBound = (x1, y1)
        self.bottomRightBound = (x2, y2)
        self.width = x2 - x1
        self.height = y2 - y1
        self.entities = [Entity(self) for i in range(self.entityCount)]
        self.image = pygame.Surface((config.width, config.height))

    def update(self):

        self.image.fill(config.colorBlack)
        pygame.draw.rect(self.image, config.colorWhite, pygame.Rect(0, 0, self.width, self.height), config.boundThickness)

        for entity in self.entities:
            entity.box = entity.box.move(entity.step)

        entityTypes = Counter()
        for entity in self.entities:
            entity.update()
            entityTypes[entity.state] += 1
            self.image.blit(entity.image, entity.box)

        # print(entityTypes)



    def infectRandom(self, count = 1):

        targets = []
        for entity in self.entities:
            if entity.state == State.SUSCEPTIBLE:
                targets.append(entity)

        for entity in sample(targets, min(len(targets), count)):
            entity.infect()