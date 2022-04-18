import config, pygame
from random import sample, random
from collections import Counter

from config import State
from entity import Entity


class simulationBasic:
    def __init__(self, entityCount=100):
        self.areas = []


    def update(self):
        for area in areas:
            area.update()