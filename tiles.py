import os
import csv
from config import tiles
from config import pygame
from config import tile_size, width, height


class TileMap:
    def __init__(self):
        self.__tiles = tiles
        self.__tile_map = []

    @staticmethod
    def draw_tile(image, surface):
        surface.blit(image, )

    def read_csv(self, filename):
        with open(os.path.join(filename)) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.__tile_map.append(list(row))
                # print(list(row))
        print(self.__tile_map)

    def draw_map(self, surface):
        for row in self.__tile_map:
            for tile in row:
                if tile != '-1':
                    image = self.__tiles[tile]
                    self.draw_tile(image, surface)

