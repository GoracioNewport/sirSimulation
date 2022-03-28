import config, pygame
from config import State

from random import randrange
from math import sqrt

class Entity:
    def __init__(self, homeArea):
        self.r = 5
        self.color = config.colorSusceptible
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
        self.timer = []

    def updateTarget(self):
        self.targetX = randrange(0, (self.area.bottomRightBound[0] - self.area.topLeftBound[0]) - self.image.get_height())
        self.targetY = randrange(0, (self.area.bottomRightBound[1] - self.area.topLeftBound[1]) - self.image.get_height())

    def update(self):

        if (self.state == State.SUSCEPTIBLE): self.color = config.colorSusceptible
        elif (self.state == State.INFECTIOUS): self.color = config.colorInfectious
        elif (self.state == State.RECOVERED): self.color = config.colorRecovered

        distSquared = (self.targetX - self.box.x) * (self.targetX - self.box.x) + (self.targetY - self.box.y) * (self.targetY - self.box.y)

        if (distSquared <= config.targetChangeDistance * config.targetChangeDistance):
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