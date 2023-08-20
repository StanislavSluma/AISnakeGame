import pygame
import os
import sys


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


tile_size = 16
width = tile_size * 62
height = tile_size * 31
running = True
game_over = False
dict_keys_unkeys = {pygame.K_w: ["up", "down"], pygame.K_UP: ["up", "down"], pygame.K_s: ["down", "up"],
                    pygame.K_DOWN: ["down", "up"], pygame.K_a: ["left", "right"], pygame.K_LEFT: ["left", "right"],
                    pygame.K_d: ["right", "left"], pygame.K_RIGHT: ["right", "left"]}

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake game Score : 0")

background_load = resource_path(os.path.join('resources/level_design', 'snakeBg.png'))
background = pygame.image.load(background_load)

apple_load = resource_path(os.path.join('resources/snake', 'apple.png'))
apple = pygame.image.load(apple_load)
orange_load = resource_path(os.path.join('resources/snake', 'orange.png'))
orange = pygame.image.load(orange_load)

snake_head_path = resource_path(os.path.join('resources/snake', 'snake_head.png'))
snake_head = pygame.image.load(snake_head_path)
snake_body_path = resource_path(os.path.join('resources/snake', 'snake_body.png'))
snake_body = pygame.image.load(snake_body_path)
snake_tail_path = resource_path(os.path.join('resources/snake', 'snake_tail.png'))
snake_tail = pygame.image.load(snake_tail_path)
snake_left_path = resource_path(os.path.join('resources/snake', 'snake_corner_left.png'))
snake_left = pygame.image.load(snake_left_path)
snake_right_path = resource_path(os.path.join('resources/snake', 'snake_corner.png'))
snake_right = pygame.image.load(snake_right_path)
menu_image_path = resource_path(os.path.join('resources', 'menu_image.jpg'))
menu_image = pygame.image.load(menu_image_path)

tile285_path = resource_path(os.path.join('resources/level_design/tiles', '285.png'))
tile285 = pygame.image.load(tile285_path)
tile305_path = resource_path(os.path.join('resources/level_design/tiles', '305.png'))
tile305 = pygame.image.load(tile305_path)
tile326_path = resource_path(os.path.join('resources/level_design/tiles', '326.png'))
tile326 = pygame.image.load(tile326_path)
tile329_path = resource_path(os.path.join('resources/level_design/tiles', '329.png'))
tile329 = pygame.image.load(tile329_path)

tiles = {'285': tile285, '305': tile305, '326': tile326, '329': tile329}
