import os
import csv
import random

from config import tiles
from config import pygame
from config import tile_size, width, height, background


class TileMap:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__tiles = tiles
        self.__tile_map = []
        self.__rock_coordinates = []
        self.__bush_coordinates = []

    @property
    def rock_coordinates(self):
        return self.__rock_coordinates

    @property
    def bush_coordinates(self):
        return self.__bush_coordinates

    def generate_tile_map(self, surface):
        self.__rock_coordinates.clear()
        self.__bush_coordinates.clear()
        surface.blit(background, (0, 0))
        generate = 100
        not_gen = [(width / 2, height / 2 + 8), (width / 2, height / 2 + 24), (width / 2, height / 2 + 40),
                   (width / 2 - tile_size, height / 2 - 8), (width / 2, height / 2 - 8),
                   (width / 2 + tile_size, height / 2 - 8)]
        while generate > -1:
            self.__x = random.randint(0, int(width / tile_size - 1))
            self.__y = random.randint(0, int(height / tile_size - 1))
            not_in_rock = (self.__x * tile_size, self.__y * tile_size) not in self.__rock_coordinates
            not_in_bush = (self.__x * tile_size, self.__y * tile_size) not in self.__bush_coordinates
            not_in_begin = (self.__x * tile_size, self.__y * tile_size) not in not_gen
            if not_in_rock and not_in_bush and not_in_begin:
                name = random.randint(1, 4)
                num = '305'
                if name == 1:
                    num = '305'
                else:
                    if name == 2:
                        num = '285'
                        self.__bush_coordinates.append((self.__x * tile_size, self.__y * tile_size))
                    else:
                        if name == 3:
                            num = '326'
                        elif name == 4:
                            num = '329'
                        self.__rock_coordinates.append((self.__x * tile_size, self.__y * tile_size))
                image = self.__tiles[num]
                surface.blit(image, (self.__x * tile_size, self.__y * tile_size))
                generate -= 1
        return surface

    def read_csv(self, filename):
        with open(os.path.join(filename)) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.__tile_map.append(list(row))

    def draw_map(self, surface):
        surface.blit(background, (0, 0))
        for row in self.__tile_map:
            self.__x = 0
            self.__y += 1
            for tile in row:
                self.__x += 1
                if tile != '-1':
                    image = self.__tiles[tile]
                    if tile != '305':
                        if tile == '329' or tile == '326':
                            self.__rock_coordinates.append((self.__x * tile_size, self.__y * tile_size))
                        elif tile == '285':
                            self.__bush_coordinates.append((self.__x * tile_size, self.__y * tile_size))
                    surface.blit(image, (self.__x * tile_size, self.__y * tile_size))
        pygame.display.update()
        return surface
