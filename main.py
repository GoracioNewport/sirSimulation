import config
from simulations.simulationBasic import SimulationBasic

import sys
import pygame

if __name__ == '__main__':

    clock = pygame.time.Clock()
    pygame.init()

    simulation = SimulationBasic(entityCount=100, maskProbability=1)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                simulation.click(x, y, event)

        config.screen.fill(config.colorBlack)
        simulation.update()

        config.screen.blit(simulation.image, simulation.boundBox[0])

        pygame.display.flip()
        clock.tick(config.frameRate)
