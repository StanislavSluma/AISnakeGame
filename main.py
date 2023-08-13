import pygame
import random
from tiles import *
from collections import namedtuple

pygame.init()

width = 992
height = 496
tile_size = 16
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake game")
running = True
Point = namedtuple('Point', 'x, y')

def bg():
    bg_image = pygame.image.load('resources/snakeBg.png').convert_alpha()
    screen.blit(bg_image, (0, 0))


class Game:
    def __init__(self):
        bg()
        self.__x = width/2
        self.__y = height/2
        self.__speed = tile_size*1
        self.__direction = ""
        self.__score = 0
        self.__place_food()
        self.clock = pygame.time.Clock()

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.__direction = "up"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.__direction = "down"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.__direction = "left"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.__direction = "right"

            self.move(self.__direction)
            self.draw_snake()
            #self.clock.tick(30)
            pygame.display.update()


    def move(self, direction):
        if direction == "up":
            self.__y += tile_size
        elif direction == "down":
            self.__y -= tile_size
        elif direction == "left":
            self.__x -= tile_size
        elif direction == "right":
            self.__x += tile_size
        print(self.__x, self.__y)

    def is_collision(self):
        pass

    def update(self):
        pass

    def __place_food(self):
        __pos = Point(random.randint(0, 61), random.randint(0, 30))
        apple = pygame.image.load('resources/apple.png')
        fruit_rect = pygame.Rect(int(__pos.x * tile_size), int(__pos.y * tile_size), tile_size, tile_size)
        screen.blit(apple, fruit_rect)

    def draw_snake(self, direction, speed):
        head_rect = pygame.Rect(100, 100, tile_size, tile_size)
        pygame.draw.rect(screen, (255, 0, 0), head_rect)


if __name__ == '__main__':
    tm = TileMap()
    tile_map = tm.read_csv('resources/snakeLevel.csv')
    print(tile_map)
    game = Game()
    pygame.display.update()
    while running:
        game.event_listener()


    pygame.quit()