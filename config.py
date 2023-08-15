import pygame

tile_size = 16
width = tile_size * 62
height = tile_size * 31
running = True
dict_keys_unkeys = {pygame.K_w: ["up", "down"], pygame.K_UP: ["up", "down"], pygame.K_s: ["down", "up"],
                    pygame.K_DOWN: ["down", "up"], pygame.K_a: ["left", "right"], pygame.K_LEFT: ["left", "right"],
                    pygame.K_d: ["right", "left"], pygame.K_RIGHT: ["right", "left"]}

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake game Score : 0")

snake_head = pygame.image.load('resources/snake/snake_head.png')
snake_body = pygame.image.load('resources/snake/snake_body.png')
snake_tail = pygame.image.load('resources/snake/snake_tail.png')
snake_left = pygame.image.load('resources/snake/snake_corner_left.png')
snake_right = pygame.image.load('resources/snake/snake_corner.png')
