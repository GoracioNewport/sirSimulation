from enum import Enum, auto
import pygame

class EventType(Enum):
    DISEASE = auto()
    INFECTION_SPREAD = auto()

class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    RECOVERED = auto()


size = width, height = 800, 640

screen = pygame.display.set_mode(size)
background = pygame.Surface(size)


frameRate = 60
targetChangeDistance = 10
boundThickness = 3

diseaseDurationMin = 500
diseaseDurationMax = 600
spreadIntervalMin = 100
spreadIntervalMax = 150
spreadRadius = 100

spreadProbability = 0.1

colorBlack = (0, 0, 0)
colorWhite = (255, 255, 255)
colorSusceptible = (0, 255, 0)
colorInfectious = (255, 0, 0)
colorRecovered = (127, 127, 127)
colorInfectRing = (150, 9, 0)

walkPatterns = [-1, 0, 1]