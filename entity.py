import math

import config, pygame
from config import State

from random import randrange, random
from math import sqrt
from event import Event


class Entity:
    def __init__(self, homeArea, id = 0, hasMask = False):
        self.r = 5
        self.id = id
        self.color = config.colorSusceptible
        self.mask = hasMask
        self.step = [.0, .0]
        self.speed = 3
        self.area = homeArea
        self.image = pygame.Surface((self.r * 2, self.r * 2))
        self.box = self.image.get_rect(topleft=(
            randrange(0, (self.area.bottomRightBound[0] - self.area.topLeftBound[0]) - self.image.get_width()),
            randrange(0, (self.area.bottomRightBound[1] - self.area.topLeftBound[1]) - self.image.get_height())))

        self.targetX = 0
        self.targetY = 0

        self.updateTarget()

        self.state = State.SUSCEPTIBLE
        self.events = []

    def updateTarget(self):
        self.targetX = randrange(0, (self.area.bottomRightBound[0] - self.area.topLeftBound[0]) - self.image.get_height())
        self.targetY = randrange(0, (self.area.bottomRightBound[1] - self.area.topLeftBound[1]) - self.image.get_height())

    def updateColor(self):
        if self.state == State.SUSCEPTIBLE:
            self.color = config.colorSusceptible

        elif self.state == State.INFECTIOUS:
            self.color = config.colorInfectious

        elif self.state == State.RECOVERED:
            self.color = config.colorRecovered

    def updateCords(self):
        distSquared = (self.targetX - self.box.x) * (self.targetX - self.box.x) + (self.targetY - self.box.y) * (self.targetY - self.box.y)

        if distSquared <= config.targetChangeDistance * config.targetChangeDistance:
            self.updateTarget()

        distX = (self.targetX - self.box.x)
        distY = (self.targetY - self.box.y)
        coefficient = distX / (distY if distY != 0 else 2e18)

        self.step[1] = sqrt((self.speed * self.speed) / ((coefficient * coefficient) + 1))
        self.step[0] = abs(coefficient) * self.step[1]

        if self.targetX < self.box.x:
            self.step[0] *= -1
        if self.targetY < self.box.y:
            self.step[1] *= -1

    def updateEvents(self):

        eventsNew = list()

        for event in self.events:

            if not event.tick():
                if event.type == config.EventType.DISEASE:
                    self.recover()

                elif event.type == config.EventType.INFECTION_SPREAD and self.state == config.State.INFECTIOUS:
                    self.spreadInfection()

            else:
                eventsNew.append(event)

        self.events = eventsNew


    def update(self):
        self.updateEvents()
        self.updateColor()
        self.updateCords()

        self.image.fill(config.colorBlack)
        pygame.draw.circle(self.image, self.color, (self.r,  self.r), self.r)

    def infect(self):
        self.state = State.INFECTIOUS
        self.events.append(Event(config.EventType.DISEASE, randrange(config.diseaseDurationMin, config.diseaseDurationMax)))
        self.events.append(Event(config.EventType.INFECTION_SPREAD, randrange(config.spreadIntervalMin, config.spreadIntervalMax)))

    def spreadInfection(self):
        self.events.append(Event(config.EventType.INFECTION_SPREAD, randrange(config.spreadIntervalMin, config.spreadIntervalMax)))


        # pygame.draw.circle(self.area.image, config.colorInfectRing, (self.area.topLeftBound[0] + self.box.x + self.r, self.area.topLeftBound[1] + self.box.y + self.r), config.spreadRadius)

        for entity in self.area.entities:
            dist = math.hypot(entity.box.x - self.box.x, entity.box.y - self.box.y)
            if dist <= config.spreadRadius and entity.state == config.State.SUSCEPTIBLE:
                if random() < config.spreadProbability[self.mask][entity.mask]:
                    entity.infect()

    def recover(self):

        self.state = State.RECOVERED
