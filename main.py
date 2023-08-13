import pygame
from tiles import *

pygame.init()
clock = pygame.time.Clock()

width = 992
height = 496
tile_size = 16
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake game")
running = True


def bg():
    bg = pygame.image.load('resources/snakeBg.png').convert_alpha()
    screen.blit(bg, (0, 0))

class Game:
    def __init__(self):
        self.__x = width/2
        self.__y = height/2
        self.__speed = 1
        self.__direction = ""
        self.__score = 0

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.__direction = "up"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.__direction = "down"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.__direction = "left"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.__direction = "right"

            self._move(self.__direction)

    def _move(self, direction):
        if direction == "up":
            self.__y += tile_size
        elif direction == "down":
            self.__y -= tile_size
        elif direction == "left":
            self.__x -= tile_size
        elif direction == "right":
            self.__x += tile_size
        print(self.__x, self.__y)

    def _is_collision(self):
        pass

    def _update(self):
        pass

    def _place_food(self):
        pass

    def _eat_food(self):
        pass


if __name__ == '__main__':
    bg()
    tm = TileMap()
    tile_map = tm.read_csv('resources/snakeLevel.csv')
    print(tile_map)
    pygame.display.update()
    game = Game()
    while running:
        game.event_listener()

    pygame.quit()