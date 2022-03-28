import sys
import pygame

from random import randrange, sample, choice
from enum import Enum, auto
from math import sqrt

size = width, height = 800, 640
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
frameRate = 100
targetChangeDistance = 10
boundThickness = 3

colorSusceptible = (0, 255, 0)
colorInfectious = (255, 0, 0)
colorRecovered = (127, 127, 127)

walkPatterns = [-1, 0, 1]

pygame.init()

class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    RECOVERED = auto()


class Entity:
    def __init__(self, homeArea):
        self.r = 5
        self.color = colorSusceptible
        self.step = [0, 0]
        self.speed = 2
        self.area = homeArea
        self.image = pygame.Surface((self.r * 2, self.r * 2))
        self.box = self.image.get_rect(topleft=(
            randrange(0, (self.area.bottomRightBound[0] - self.area.topLeftBound[0]) - self.image.get_width()),
            randrange(0, (self.area.bottomRightBound[1] - self.area.topLeftBound[1]) - self.image.get_height())))

        self.targetX = 0
        self.targetY = 0

        self.updateTarget()

        self.state = State.SUSCEPTIBLE

    def updateTarget(self):
        self.targetX = randrange(0, (self.area.bottomRightBound[0] - self.area.topLeftBound[0]) - self.image.get_height())
        self.targetY = randrange(0, (self.area.bottomRightBound[1] - self.area.topLeftBound[1]) - self.image.get_height())

    def update(self):

        if (self.state == State.SUSCEPTIBLE): self.color = colorSusceptible
        elif (self.state == State.INFECTIOUS): self.color = colorInfectious
        elif (self.state == State.RECOVERED): self.color = colorRecovered

        distSquared = (self.targetX - self.box.x) * (self.targetX - self.box.x) + (self.targetY - self.box.y) * (self.targetY - self.box.y)

        if (distSquared <= targetChangeDistance * targetChangeDistance):
            self.updateTarget()

        distX = (self.targetX - self.box.x)
        distY = (self.targetY - self.box.y)
        cooficent = distX / (distY if distY != 0 else 2e18)

        self.step[1] = sqrt((self.speed * self.speed) / ((cooficent * cooficent) + 1))
        self.step[0] = abs(cooficent) * self.step[1]

        if self.targetX < self.box.x:
            self.step[0] *= -1
        if self.targetY < self.box.y:
            self.step[1] *= -1

        pygame.draw.circle(self.image, self.color, (self.r,  self.r), self.r)

    def infect(self):

        self.state = State.INFECTIOUS

class Area:
    def __init__(self, entityCount, x1, y1, x2, y2):
        self.entityCount = entityCount
        self.topLeftBound = (x1, y1)
        self.bottomRightBound = (x2, y2)
        self.width = x2 - x1
        self.height = y2 - y1
        self.entities = [Entity(self) for i in range(self.entityCount)]
        self.image = pygame.Surface((width, height))

    def update(self):

        self.image.fill(black)
        pygame.draw.rect(self.image, white, pygame.Rect(0, 0, self.width, self.height), boundThickness)

        for entity in self.entities:
            entity.box = entity.box.move(entity.step)

        for entity in self.entities:
            entity.update()
            self.image.blit(entity.image, entity.box)

    def infectRandom(self, count = 1):

        targets = []
        for entity in self.entities:
            if (entity.state == State.SUSCEPTIBLE):
                targets.append(entity)

        for entity in sample(targets, min(len(targets), count)):
            entity.infect()

# areas = [Area(50, 10, 10, width - 10, height - 10)]
# areas[0].infectRandom(10)

areas = [
    Area(50, 0, 0, width / 2, height / 2),
    Area(50, width / 2, height / 2, width, height)
]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            for area in areas:
                if (x >= area.topLeftBound[0] and x <= area.bottomRightBound[0] and y >= area.topLeftBound[1] and y <= area.bottomRightBound[1]):
                    area.infectRandom()

    screen.fill(black)

    for area in areas:
        area.update()
        screen.blit(area.image, area.topLeftBound)


    pygame.display.flip()
    clock.tick(frameRate)
