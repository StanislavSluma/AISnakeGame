import random

import pygame.image

from config import tile_size, screen, width, height


class Food:

    def __init__(self):
        self.__food_x = 0
        self.__food_y = 0
        self.__food = False
        self.place_food()

    @property
    def food(self):
        return self.__food

    @food.setter
    def food(self, value):
        self.__food = value

    def get_food_point(self):
        return self.__food_x * tile_size, self.__food_y * tile_size

    def place_food(self):
        if not self.__food:
            self.__food_x = random.randint(0, width / tile_size - 1)
            self.__food_y = random.randint(0, height / tile_size - 1)
            self.__food = True
        apple = pygame.image.load('resources/snake/apple.png')
        fruit_rect = pygame.Rect(int(self.__food_x * tile_size), int(self.__food_y * tile_size), tile_size, tile_size)
        screen.blit(apple, fruit_rect)
