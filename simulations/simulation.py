import config, pygame
from area import Area


class Simulation:
    def __init__(self,
                 boundBox=((0, 0), (config.width, config.height)),
                 maskProbability=0, quarantineMode=False):

        self.areas = []
        self.quarantineArea = Area()
        self.quarantineMode = quarantineMode
        self.maskProbability = maskProbability
        self.boundBox = boundBox

        self.width = boundBox[1][0] - boundBox[0][0]
        self.height = boundBox[1][1] - boundBox[0][1]
        self.image = pygame.Surface((self.width, self.height))



    def update(self):

        self.image.fill(config.colorBlack)

        for area in self.areas:
            area.update()
            self.image.blit(area.image, area.boundBox[0])

    def click(self, x, y, event):

        for area in self.areas:
            if area.boundBox[0][0] <= x <= area.boundBox[1][0] and area.boundBox[0][1] <= y <= area.boundBox[1][1]:
                if event.button == 4:
                    area.reset()

                else:
                    area.infectRandom()