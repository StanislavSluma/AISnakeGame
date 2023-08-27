import random

from config import tile_size, screen, width, height, apple, orange


class Food:

    def __init__(self):
        self.__food_x = 0
        self.__food_y = 0
        self.__type_food = 'apple'
        self.__timer = 0
        self.__food = False

    @property
    def food(self):
        return self.__food

    @food.setter
    def food(self, food):
        self.__food = food

    @property
    def type_food(self):
        return self.__type_food

    def get_food_point(self):
        return (self.__food_x * tile_size, self.__food_y * tile_size)

    def place_food(self, tiles, all_snake):
        if self.__timer == 1:
            self.__food = False
        if self.__timer > 0:
            self.__timer -= 1
        if not self.__food:
            self.__timer = 0
            if random.randint(1, 8) == 1:
                self.__type_food = 'orange'
                self.__timer = 65
            else:
                self.__type_food = 'apple'
            self.__food_x = random.randint(0, width / tile_size - 1)
            self.__food_y = random.randint(0, height / tile_size - 1)
            in_tile = (self.__food_x * tile_size, self.__food_y * tile_size) in tiles
            in_snake = False
            for body in all_snake:
                in_snake = (((self.__food_x * tile_size, self.__food_y * tile_size) == body) or in_snake)
            while in_snake or in_tile:
                self.__food_x = random.randint(0, width / tile_size - 1)
                self.__food_y = random.randint(0, height / tile_size - 1)
                in_tile = (self.__food_x * tile_size, self.__food_y * tile_size) in tiles
                in_snake = (self.__food_x * tile_size, self.__food_y * tile_size) in all_snake
            self.__food = True
        if self.__type_food == 'apple':
            screen.blit(apple, (self.__food_x * tile_size, self.__food_y * tile_size))
        else:
            screen.blit(orange, (self.__food_x * tile_size, self.__food_y * tile_size))
