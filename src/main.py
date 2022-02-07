from graphics import Screen
from input import Input
import sys
import threading
import pygame

pygame.init()

def main():
    input = Input()
    input_thread = threading.Thread(target = input.sampling)
    input_thread.daemon = True
    input_thread.start()

    screen = Screen()
    running = True
    while running:
        print(input.get_frequency())
        pygame.time.Clock().tick(128)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.update()
        screen.draw()
    input.stop()

main()

pygame.quit()