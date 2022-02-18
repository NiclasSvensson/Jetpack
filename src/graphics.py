import pygame
from random import randint
from constants import *

class Assets():
    def __init__(self):
        self.sand = pygame.image.load("../assets/sand.png")
        self.water = pygame.image.load("../assets/water.png")
        self.submarine = pygame.image.load("../assets/submarine.png")
        self.mine = pygame.image.load("../assets/mines.png")
        self.explosion = pygame.image.load("../assets/explosion.png")
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
        self.v = 0
        self.g = 15

    def update(self, frequency, bottom):
        if self.rect.bottom > bottom - BLOCK + 20:
            self.v = 0
            self.rect.bottom = bottom - BLOCK + 20
        elif self.rect.top <= bottom - BLOCK * DEPTH:
            self.v = self.v + (self.g*10)*dt
            self.rect.y += int(self.v*dt)
        else:
            self.v = min(50, self.v + (self.g - frequency/6)*dt)
            self.rect.y += int(self.v*dt)

class Mine(pygame.sprite.Sprite):
    def __init__(self, screen, assets, y):
        super().__init__()
        self.screen = screen
        self.image = assets.mine
        self.assets = assets
        self.rect = self.image.get_rect() 
        self.rect.center = (pygame.display.get_window_size()[0] + BLOCK, y)

    def update(self):
        if self.rect.x < -BLOCK:
            self.kill()
        self.rect.x -= 4

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

        self.mines = pygame.sprite.Group()
        self.start_time = pygame.time.get_ticks()

    def update(self, frequency):
        self.water.update()
        self.submarine_sprite.update(frequency, self.size[1])
        self.mines.update()
        self.sand.update()
        hit_bomb = pygame.sprite.spritecollide(self.submarine, self.mines, True)
        if hit_bomb:
            print(hit_bomb[0].rect.y)
        if pygame.time.get_ticks() - self.start_time > BOMB_FREQUENCY:
            self.start_time = pygame.time.get_ticks()
            self.mines.add(Mine(self.screen, self.assets, randint(self.size[1] - BLOCK*DEPTH + BLOCK, self.size[1] - BLOCK)))

    def draw(self):
        self.screen.fill(self.background_color)
        self.water.draw()
        self.sand.draw()
        self.mines.draw(self.screen)
        self.submarine_sprite.draw(self.screen)
        pygame.display.flip()
