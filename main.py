import config

from area import Area

import sys
import pygame

if __name__ == '__main__':

    clock = pygame.time.Clock()
    pygame.init()

    areas = [
        Area(100, 0, 0, config.width, config.height, 0.5)
    ]

    statisticsData = []

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                for area in areas:
                    if area.topLeftBound[0] <= x <= area.bottomRightBound[0] and area.topLeftBound[1] <= y <= area.bottomRightBound[1]:
                        area.reset()

        for area in areas:
            area.update()
            config.screen.blit(area.image, area.topLeftBound)

            if (area.simulationOver):
                statisticsData.append(area.diseaseSpan // 100)
                if (len(statisticsData) >= 15):
                    print(statisticsData)
                    sys.exit()
                area.reset()


        pygame.display.flip()
        clock.tick(config.frameRate)
