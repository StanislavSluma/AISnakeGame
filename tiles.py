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
        self.__tile_coordinates = []

    @property
    def tile_coordinates(self):
        return self.__tile_coordinates

    def generate_tile_map(self, surface):
        self.__tile_coordinates.clear()
        surface.blit(background, (0, 0))
        generate = 100
        not_gen = [(width / 2, height / 2 + 8), (width / 2, height / 2 + 24), (width / 2, height / 2 + 40),
                   (width / 2 - tile_size, height / 2 - 8), (width / 2, height / 2 - 8),
                   (width / 2 + tile_size, height / 2 - 8)]
        while generate > -1:
            self.__x = random.randint(0, width / tile_size - 1)
            self.__y = random.randint(0, height / tile_size - 1)
            if (self.__x * tile_size, self.__y * tile_size) not in not_gen and (self.__x * tile_size, self.__y * tile_size) not in self.__tile_coordinates:
                name = random.randint(1, 4)
                if name == 1:
                    num = '305'
                else:
                    if name == 2:
                        num = '285'
                    elif name == 3:
                        num = '326'
                    elif name == 4:
                        num = '329'
                    self.__tile_coordinates.append((self.__x * tile_size, self.__y * tile_size))
                image = self.__tiles[num]
                surface.blit(image, (self.__x * tile_size, self.__y * tile_size))
                generate -= 1
        return surface

    def read_csv(self, filename):
        with open(os.path.join(filename)) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.__tile_map.append(list(row))
        print(self.__tile_map)

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
                        self.__tile_coordinates.append((self.__x * tile_size, self.__y * tile_size))
                    surface.blit(image, (self.__x * tile_size, self.__y * tile_size))
        pygame.display.update()
        return surface
