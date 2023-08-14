import pygame
from collections import namedtuple

width = 992
height = 496
tile_size = 16

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake game Score : 0")

Point = namedtuple('Point', 'x, y')

running = True

snake_head = pygame.image.load('resources/snake/snake_head.png')
snake_body = pygame.image.load('resources/snake/snake_body.png')
snake_tail = pygame.image.load('resources/snake/snake_tail.png')
