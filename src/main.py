from graphics import Screen
from input import Input
import sys
import pygame

pygame.init()

def main():
    #input = Input()
    #while True:
    #    f = input.get_frequency()
    #    print(f)
    screen = Screen()
    while 1:
        pygame.time.Clock().tick(128)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        screen.update()
        screen.draw()

main()