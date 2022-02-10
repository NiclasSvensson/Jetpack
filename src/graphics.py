import pygame
from random import randint
from constants import *

class Assets():
    def __init__(self):
        self.sand = pygame.image.load("../assets/sand.png")
        self.water = pygame.image.load("../assets/water.png")
        self.submarine = pygame.image.load("../assets/submarine.png")
        self.rects = [pygame.Rect(0, x*BLOCK, BLOCK, BLOCK) for x in range(6)]

    def get_rect(self, i):
        return self.rects[i]

class Sand():
    def __init__(self, screen, assets, width, y_pos):
        self.screen = screen
        self.assets = assets
        self.lst = [[BLOCK*(x-1), randint(0, 5)] for x in range(width)]
        self.y_pos = y_pos - BLOCK
    
    def update(self):
        for i in self.lst:
            if i[0] <= -BLOCK:
                i[0] = pygame.display.get_window_size()[0] - 4
            else:
                i[0] -= 4

    def draw(self):
        for i in self.lst:
            self.screen.blit(self.assets.sand, (i[0], self.y_pos), self.assets.get_rect(i[1]))

class Water():
    def __init__(self, screen, assets, width):
        self.screen = screen
        self.assets = assets
        self.lst = [[[BLOCK*(x-1), pygame.display.get_window_size()[1] - DEPTH*BLOCK + y*BLOCK ,0 if y == 0 else 1] for x in range(width)] for y in range(DEPTH)]

    def update(self):
        for y in self.lst:
            for x in y:
                if x[0] <= -BLOCK:
                    x[0] = pygame.display.get_window_size()[0] - 1
                else:
                    x[0] -= 1

    def draw(self):
        for y in self.lst:
            for x in y:
                self.screen.blit(self.assets.water, (x[0], x[1]), self.assets.get_rect(x[2]))

class Submarine(pygame.sprite.Sprite):
    def __init__(self, screen, assets, x, y):
        super().__init__()
        self.screen = screen
        self.image = assets.submarine
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y)      

    def update(self, frequency, bottom):
        if frequency > 0.1:
            self.rect.y -= (frequency / 100)
        elif self.rect.bottom >= bottom - BLOCK + 20:
            pass
        else:
            self.rect.y += 2

class Mine():
    def __init__(self):
        pass

class Screen():
    def __init__(self):
        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.size = pygame.display.get_window_size()
        self.background_color = 0, 177, 217
        self.block_size = (self.size[0]//BLOCK + 1, self.size[1]//BLOCK + 1)
        self.assets = Assets()

        self.sand = Sand(self.screen, self.assets, self.block_size[0], self.size[1])
        self.water = Water(self.screen, self.assets, self.block_size[0])
        self.submarine = Submarine(self.screen, self.assets, 3*BLOCK, self.size[1] - DEPTH*BLOCK/2)

        self.submarine_sprite = pygame.sprite.Group()
        self.submarine_sprite.add(self.submarine)

    def update(self, frequency):
        self.water.update()
        self.submarine_sprite.update(frequency, self.size[1])
        self.sand.update()

    def draw(self):
        self.screen.fill(self.background_color)
        self.water.draw()
        self.sand.draw()
        self.submarine_sprite.draw(self.screen)
        pygame.display.flip()
