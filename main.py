import random

import pygame

from tiles import *
from config import *

pygame.init()
pygame.mixer.music.load('resources/sounds/mixkit-game-level-music-689.wav')
pygame.mixer.music.load('resources/sounds/mixkit-game-ball-tap-2073.wav', 'ate')
pygame.mixer.Channel(0).play(pygame.mixer.Sound('resources/sounds/mixkit-game-level-music-689.wav'))

'''
class Snake:
    def __init__(self):
        self.__snake_body = [(width/2, height/2 + 8), (width/2, height/2 + 24), (width/2, height/2 + 40)]
'''


class Game:
    def __init__(self):
        self.__x = width/2
        self.__y = height/2 + 8
        self.__snake_body = [(width / 2, height / 2 + 8), (width / 2, height / 2 + 24), (width / 2, height / 2 + 40)]
        self.__speed = 8
        self.__direction = "up"
        self.__score = 0
        self.__event = False
        self.food = False
        self.food_x = 0
        self.food_y = 0
        self.bg()
        self.clock = pygame.time.Clock()

    def bg(self):
        background = pygame.image.load('resources/level_design/snakeBg.png').convert_alpha()
        screen.blit(background, (0, 0))
        self.__place_food()

    def event_listener(self):
        old_direction = ''
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.__direction = "up"
                    if old_direction != self.__direction:
                        self.__event = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.__direction = "down"
                    if old_direction != self.__direction:
                        self.__event = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.__direction = "left"
                    if old_direction != self.__direction:
                        self.__event = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.__direction = "right"
                    if old_direction != self.__direction:
                        self.__event = True

        self.move(self.__direction)
        self.__check_for_food()
        self.draw_snake()
        self.clock.tick(self.__speed)
        pygame.display.update()

    def __check_for_food(self):
        if self.__x == self.food_x * tile_size and self.__y == self.food_y * tile_size:
            self.food = False
            self.__score += 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('resources/sounds/mixkit-game-ball-tap-2073.wav'))
            pygame.display.set_caption(f"Snake game Score : {self.__score}")
            if self.__score > 10:
                self.__speed += 1
            self.__snake_body.append(self.__snake_body[-1])
            print(self.__score)

    def move(self, direction):
        if direction == "up":
            self.__y -= tile_size
        elif direction == "down":
            self.__y += tile_size
        elif direction == "left":
            self.__x -= tile_size
        elif direction == "right":
            self.__x += tile_size

    def is_collision(self):
        pass

    def __place_food(self):
        if not self.food:
            self.food_x = random.randint(0, 61)
            self.food_y = random.randint(0, 30)
            self.food = True
        apple = pygame.image.load('resources/snake/apple.png')
        fruit_rect = pygame.Rect(int(self.food_x * tile_size), int(self.food_y * tile_size), tile_size, tile_size)
        screen.blit(apple, fruit_rect)

    def draw_snake(self):
        self.bg()
        if self.__direction != '':
            new_body = list.copy(self.__snake_body)
            new_body[0] = (self.__x, self.__y)
            new_body[1:] = self.__snake_body[0:-1]
            self.__snake_body = new_body

        global snake_head, snake_body, snake_tail
        if self.__event and self.__direction == 'right':
            print(self.__event)
            snake_head = pygame.transform.rotate(snake_head, 270)
            snake_body = pygame.transform.rotate(snake_body, 90)
            snake_tail = pygame.transform.rotate(snake_tail, 270)
            self.__event = False
        elif self.__event and self.__direction == 'left':
            print(self.__event)
            snake_head = pygame.transform.rotate(snake_head, -270)
            snake_body = pygame.transform.rotate(snake_body, 90)
            snake_tail = pygame.transform.rotate(snake_tail, -270)
            self.__event = False
        elif self.__event and self.__direction == 'up':
            print(self.__event)
            snake_head = pygame.transform.rotate(snake_head, 90)
            snake_body = pygame.transform.rotate(snake_body, -90)
            snake_tail = pygame.transform.rotate(snake_tail, 90)
            self.__event = False
        elif self.__event and self.__direction == 'down':
            print(self.__event)
            snake_head = pygame.transform.rotate(snake_head, -90)
            snake_body = pygame.transform.rotate(snake_body, 90)
            snake_tail = pygame.transform.rotate(snake_tail, -90)
            self.__event = False

        head_rect = pygame.Rect(self.__snake_body[0][0], self.__snake_body[0][1], tile_size, tile_size)
        screen.blit(snake_head, head_rect)

        for point in self.__snake_body[1:-1]:
            body_rect = pygame.Rect(point[0], point[1], tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), body_rect)
            screen.blit(snake_body, body_rect)

        tail_rect = pygame.Rect(self.__snake_body[-1][0], self.__snake_body[-1][1], tile_size, tile_size)
        screen.blit(snake_tail, tail_rect)


if __name__ == '__main__':
    tm = TileMap()
    tile_map = tm.read_csv('resources/level_design/snakeLevel.csv')
    # print(tile_map)
    game = Game()
    pygame.display.update()
    global running
    while running:
        game.event_listener()

    pygame.quit()
