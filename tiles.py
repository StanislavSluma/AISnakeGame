import os
import csv
from config import tiles
from config import pygame
from config import tile_size, width, height, screen, background


class TileMap:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__tiles = tiles
        self.__tile_map = []

    def __generate_tile_map(self):
        pass

    def read_csv(self, filename):
        with open(os.path.join(filename)) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.__tile_map.append(list(row))
        print(self.__tile_map)

    def draw_map(self, surface):
        surface.blit(background, (0, 0))
        for row in self.__tile_map:
            self.__y = 0
            self.__x += 1
            for tile in row:
                self.__y += 1
                if tile != '-1':
                    print(tile)
                    image = self.__tiles[tile]
                    surface.blit(image, (self.__y * tile_size, self.__x * tile_size))
        self.__x = 0
        self.__y = 0
        pygame.display.update()
        return surface