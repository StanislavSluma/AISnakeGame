import pygame.draw
import pygame.transform

from config import width, height, tile_size, screen, snake_head, snake_body, snake_tail, snake_left, snake_right


class Snake:
    def __init__(self):
        self.__x = width/2
        self.__y = height/2 + 8
        self.__snake_body = [
            [width / 2, height / 2 + 8, 0], [width / 2, height / 2 + 24, 0], [width / 2, height / 2 + 40, 0]
        ]
        self.__speed = 8
        self.draw_snake('')

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        if speed > 0:
            self.__speed = speed

    def get_place_head(self):
        return self.__x, self.__y

    def move(self, direction):
        if direction == "up":
            if self.__y == 0:
                self.__y = height - tile_size
            else:
                self.__y -= tile_size
        elif direction == "down":
            if self.__y == height - tile_size:
                self.__y = 0
            else:
                self.__y += tile_size
        elif direction == "left":
            if self.__x == 0:
                self.__x = width - tile_size
            else:
                self.__x -= tile_size
        elif direction == "right":
            if self.__x == width - tile_size:
                self.__x = 0
            else:
                self.__x += tile_size

    def is_collision(self, tiles):
        head = self.get_place_head()
        for body in self.__snake_body[1:]:
            if head == (body[0], body[1]):
                return True
        if head in tiles:
            return True
        return False

    def ate(self):
        self.__snake_body.append(self.__snake_body[-1])

    def draw_snake(self, direction):
        if direction != '':
            new_body = list.copy(self.__snake_body)
            rotate = 0
            if direction == 'up':
                rotate = 0
            elif direction == 'left':
                rotate = 90
            elif direction == 'down':
                rotate = 180
            elif direction == 'right':
                rotate = 270
            new_body[0] = [self.__x, self.__y, rotate]
            new_body[1:] = self.__snake_body[0:-1]
            self.__snake_body = new_body

        head_rect = pygame.Rect(self.__snake_body[0][0], self.__snake_body[0][1], tile_size, tile_size)
        screen.blit(pygame.transform.rotate(snake_head, self.__snake_body[0][2]), head_rect)

        i = 1
        for body in self.__snake_body[1:-1]:
            corner = self.__snake_body[i - 1][2] - self.__snake_body[i][2]
            # left rotate
            if corner == 90 or corner == -270:
                body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
                pygame.draw.rect(screen, (255, 200, 50), body_rect, 2, 10)
                screen.blit(pygame.transform.rotate(snake_left, body[2]), body_rect)
            # right rotate
            elif corner == -90 or corner == 270:
                body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
                pygame.draw.rect(screen, (255, 200, 50), body_rect, 2, 10)
                screen.blit(pygame.transform.rotate(snake_right, body[2]), body_rect)
            else:
                body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
                pygame.draw.rect(screen, (255, 200, 50), body_rect, 2, 10)
                screen.blit(pygame.transform.rotate(snake_body, body[2]), body_rect)
            i += 1
        self.__snake_body[-1][2] = self.__snake_body[-2][2]
        tail_rect = pygame.Rect(self.__snake_body[-1][0], self.__snake_body[-1][1], tile_size, tile_size)
        screen.blit(pygame.transform.rotate(snake_tail, self.__snake_body[-1][2]), tail_rect)
