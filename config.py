from enum import Enum, auto

class EventType(Enum):
    DISEASE = auto()
    INFECT = auto()

class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    RECOVERED = auto()


size = width, height = 800, 640

black = (0, 0, 0)
white = (255, 255, 255)
frameRate = 100
targetChangeDistance = 10
boundThickness = 3

colorSusceptible = (0, 255, 0)
colorInfectious = (255, 0, 0)
colorRecovered = (127, 127, 127)

walkPatterns = [-1, 0, 1]