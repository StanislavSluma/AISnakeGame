import pygame

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

background = pygame.image.load('resources/level_design/snakeBg.png')

apple = pygame.image.load('resources/snake/apple.png')
orange = pygame.image.load('resources/snake/orange.png')

snake_head = pygame.image.load('resources/snake/snake_head.png')
snake_body = pygame.image.load('resources/snake/snake_body.png')
snake_tail = pygame.image.load('resources/snake/snake_tail.png')
snake_left = pygame.image.load('resources/snake/snake_corner_left.png')
snake_right = pygame.image.load('resources/snake/snake_corner.png')
menu_image = pygame.image.load('resources/menu_image.jpg')

tile285 = pygame.image.load('resources/level_design/tiles/285.png')
tile305 = pygame.image.load('resources/level_design/tiles/305.png')
tile326 = pygame.image.load('resources/level_design/tiles/326.png')
tile329 = pygame.image.load('resources/level_design/tiles/329.png')

tiles = {'285': tile285, '305': tile305, '326': tile326, '329': tile329}
