import config, pygame
from area import Area


class Simulation:
    def __init__(self,
                 boundBox=((0, 0), (config.width, config.height)),
                 maskProbability=0, quarantineMode=False, entityCount=0):

        self.maskProbability = maskProbability
        self.boundBox = boundBox
        self.entityCount = entityCount
        self.areas = list()
        self.events = list()

        self.width = boundBox[1][0] - boundBox[0][0]
        self.height = boundBox[1][1] - boundBox[0][1]
        self.image = pygame.Surface((self.width, self.height))

        self.quarantineMode = quarantineMode
        self.quarantineAreaIndex = -1
        self.quarantineTransferList = dict()


    def updateCords(self):

        self.image.fill(config.colorBlack)

        for area in self.areas:

            area.update()
            self.image.blit(area.image, area.boundBox[0])


        for entity in self.areas[self.quarantineAreaIndex].entities:
            if (entity.state == config.State.RECOVERED):
                self.transferEntity(self.areas[self.quarantineAreaIndex], self.quarantineTransferList[entity], entity)
                del self.quarantineTransferList[entity]


    def updateEvents(self):

        for event in self.events[:]:

            if not event.tick():
                if event.type == config.EventType.QUARANTINE_CONTAIN:
                    self.transferEntity(event.data['homeArea'], self.areas[self.quarantineAreaIndex], event.data['target'])
                    self.quarantineTransferList[event.data['target']] = event.data['homeArea']

                self.events.remove(event)

    def update(self):

        self.updateEvents()
        self.updateCords()


    def click(self, x, y, event):

        for area in self.areas:
            if area.boundBox[0][0] <= x <= area.boundBox[1][0] and area.boundBox[0][1] <= y <= area.boundBox[1][1]:
                if event.button == 4:
                    self.reset()

                else:
                    area.infectRandom()

    def reset(self):
        self.__init__(self.boundBox, self.maskProbability, self.quarantineMode)

    def initQuarantineZone(self):

        if self.quarantineMode:
            self.quarantineAreaIndex = len(self.areas)
            self.areas.append(Area(self, boundBox=((self.boundBox[0][0] + config.globalMargin, self.boundBox[1][1] - config.globalMargin - config.quarantineAreaSize),
                                                 (self.boundBox[0][0] + config.globalMargin + config.quarantineAreaSize, self.boundBox[1][1] - config.globalMargin))))

    def transferEntity(self, homeArea, newArea, entity):

        newArea.entities.append(entity)
        homeArea.entities.remove(entity)
        entity.area = newArea
        entity.updateTarget()
        entity.moveToCenter()
