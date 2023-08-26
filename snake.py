import pygame.draw
import pygame.transform

from config import width, height, tile_size, screen, snake_head, snake_body, snake_tail, snake_left, snake_right


class Snake:
    def __init__(self):
        self._x = width / 2
        self._y = height / 2 + 8
        self._snake_body = [
            [width / 2, height / 2 + 8, 0], [width / 2, height / 2 + 24, 0], [width / 2, height / 2 + 40, 0]
        ]
        self._speed = 8
        self._in_bush = 0
        self.draw_snake('')

    @property
    def speed(self):
        return self._speed

    @property
    def snake_body(self):
        return self._snake_body

    def snake_body_xy(self):
        snake_coordinates = []
        for body in self._snake_body:
            snake_coordinates.append((int(body[0]), int(body[1])))
        return snake_coordinates

    @speed.setter
    def speed(self, speed):
        if speed > 0:
            self._speed = speed

    def get_place_head(self):
        return self._x, self._y

    def move(self, direction):
        if direction == "up":
            if self._y == 0:
                self._y = height - tile_size
            else:
                self._y -= tile_size
        elif direction == "down":
            if self._y == height - tile_size:
                self._y = 0
            else:
                self._y += tile_size
        elif direction == "left":
            if self._x == 0:
                self._x = width - tile_size
            else:
                self._x -= tile_size
        elif direction == "right":
            if self._x == width - tile_size:
                self._x = 0
            else:
                self._x += tile_size

    def is_in_bush(self, bush_coord):
        head = self.get_place_head()
        if head in bush_coord:
            if self._in_bush == 0:
                self._speed /= 2
            self._in_bush = len(self._snake_body)
        if self._in_bush == 1:
            self._speed *= 2
        if self._in_bush > 0:
            self._in_bush -= 1

    def is_collision(self, rock_coord):
        head = self.get_place_head()
        for body in self._snake_body[1:]:
            if head == (body[0], body[1]):
                return True
        if head in rock_coord:
            return True
        return False

    def ate(self, delta, type_food):
        if self._in_bush > 0:
            self._speed += delta / 2
        else:
            self._speed += delta
        if type_food == 'orange':
            if self._in_bush > 0:
                self._in_bush -= 1
            if len(self._snake_body) > 3:
                self._snake_body.pop()
                self._snake_body.pop()
        else:
            self._snake_body.append(self._snake_body[-1])
            if self._in_bush > 0:
                self._in_bush += 1

    def draw_snake(self, direction):
        if self._in_bush == 0:
            color = (255, 200, 50)
        else:
            color = (255, 0, 0)
        if direction != '':
            new_body = list.copy(self._snake_body)
            rotate = 0
            if direction == 'up':
                rotate = 0
            elif direction == 'left':
                rotate = 90
            elif direction == 'down':
                rotate = 180
            elif direction == 'right':
                rotate = 270
            new_body[0] = [self._x, self._y, rotate]
            new_body[1:] = self._snake_body[0:-1]
            self._snake_body = new_body

        head_rect = pygame.Rect(self._snake_body[0][0], self._snake_body[0][1], tile_size, tile_size)
        screen.blit(pygame.transform.rotate(snake_head, self._snake_body[0][2]), head_rect)

        i = 1
        for body in self._snake_body[1:-1]:
            corner = self._snake_body[i - 1][2] - self._snake_body[i][2]
            # left rotate
            if corner == 90 or corner == -270:
                body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
                pygame.draw.rect(screen, color, body_rect, 2, 10)
                screen.blit(pygame.transform.rotate(snake_left, body[2]), body_rect)
            # right rotate
            elif corner == -90 or corner == 270:
                body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
                pygame.draw.rect(screen, color, body_rect, 2, 10)
                screen.blit(pygame.transform.rotate(snake_right, body[2]), body_rect)
            else:
                body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
                pygame.draw.rect(screen, color, body_rect, 2, 10)
                screen.blit(pygame.transform.rotate(snake_body, body[2]), body_rect)
            i += 1

        self._snake_body[-1][2] = self._snake_body[-2][2]
        tail_rect = pygame.Rect(self._snake_body[-1][0], self._snake_body[-1][1], tile_size, tile_size)
        screen.blit(pygame.transform.rotate(snake_tail, self._snake_body[-1][2]), tail_rect)