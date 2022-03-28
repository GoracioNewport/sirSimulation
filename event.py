from enum import Enum, auto


class Event:
    def __init__(self, type, timer):
        self.type = type
        self.timer = timer

    def tick(self):
        self.timer -= 1
        return self.timer > 0