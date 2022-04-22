class Event:
    def __init__(self, type, timer, data={}):
        self.type = type
        self.timer = timer
        self.data = data

    def tick(self):
        self.timer -= 1
        return self.timer > 0
