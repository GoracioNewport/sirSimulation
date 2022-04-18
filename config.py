from enum import Enum, auto
import pygame

class EventType(Enum):
    DISEASE = auto()
    INFECTION_SPREAD = auto()

class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    RECOVERED = auto()


size = width, height = 1000, 800

screen = pygame.display.set_mode(size)
background = pygame.Surface(size)


frameRate = 60
targetChangeDistance = 10

diseaseDurationMin = 1000
diseaseDurationMax = 1500
spreadIntervalMin = 30
spreadIntervalMax = 40
spreadRadius = 50

spreadProbability = [
    [0.9, 0.3],
    [0.05, 0.015]
]

colorBlack = (0, 0, 0)
colorWhite = (255, 255, 255)
colorSusceptible = (0, 255, 0)
colorInfectious = (255, 0, 0)
colorRecovered = (127, 127, 127)
colorInfectRing = (150, 9, 0)

walkPatterns = [-1, 0, 1]