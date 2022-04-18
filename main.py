import config

from simulations import simulationBasic

import sys
import pygame

if __name__ == '__main__':

    clock = pygame.time.Clock()
    pygame.init()

    simulation = simulationBasic(entityCount=150,
                        boundBox=((0, 0), (config.width, config.height)),
                        maskProbability=0)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                for area in areas:
                    if area.topLeftBound[0] <= x <= area.bottomRightBound[0] and area.topLeftBound[1] <= y <= area.bottomRightBound[1]:
                        if event.button == 4:
                            area.reset()

                        else:
                            area.infectRandom()

        config.screen.fill(config.colorBlack)
        simulation.update()

        config.screen.blit(simulation.image, simulation.topLeftBound)


        pygame.display.flip()
        clock.tick(config.frameRate)
