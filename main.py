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


'''
class Snake:
    def __init__(self):
        self.__snake_body = [(width/2, height/2 + 8), (width/2, height/2 + 24), (width/2, height/2 + 40)]
'''


class Game:
    def __init__(self):
        self.__x = width/2
        self.__y = height/2 + 8
        self.__snake_body = [(width / 2, height / 2 + 8), (width / 2, height / 2 + 24), (width / 2, height / 2 + 40)]
        self.__speed = 8
        self.__direction = ""
        self.__score = 0
        self.food = False
        self.food_x = 0
        self.food_y = 0
        self.bg()
        self.clock = pygame.time.Clock()

    def bg(self):
        background = pygame.image.load('resources/snakeBg.png').convert_alpha()
        screen.blit(background, (0, 0))
        self.__place_food()

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
        if self.__x == self.food_x * tile_size and self.__y == self.food_y * tile_size:
            self.food = False
            self.__score += 1
            if self.__score > 10:
                self.__speed += 1
            self.__snake_body.append(self.__snake_body[-1])
            print(self.__score)
        self.draw_snake()
        self.clock.tick(self.__speed)
        pygame.display.update()

    def move(self, direction):
        if direction == "up":
            self.__y -= tile_size
        elif direction == "down":
            self.__y += tile_size
        elif direction == "left":
            self.__x -= tile_size
        elif direction == "right":
            self.__x += tile_size

    def is_collision(self):
        pass

    def __place_food(self):
        if not self.food:
            self.food_x = random.randint(0, 61)
            self.food_y = random.randint(0, 30)
            self.food = True
        apple = pygame.image.load('resources/apple.png')
        fruit_rect = pygame.Rect(int(self.food_x * tile_size), int(self.food_y * tile_size), tile_size, tile_size)
        screen.blit(apple, fruit_rect)

    def draw_snake(self):
        self.bg()
        if self.__direction != '':
            new_body = list.copy(self.__snake_body)
            new_body[0] = (self.__x, self.__y)
            new_body[1:] = self.__snake_body[0:-1]
            self.__snake_body = new_body
        for point in self.__snake_body:
            body_rect = pygame.Rect(point[0], point[1], tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), body_rect)


if __name__ == '__main__':
    tm = TileMap()
    tile_map = tm.read_csv('resources/snakeLevel.csv')
    # print(tile_map)
    game = Game()
    pygame.display.update()
    while running:
        game.event_listener()

    pygame.quit()
