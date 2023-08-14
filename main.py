import random

from tiles import *
from config import *

pygame.init()
pygame.mixer.music.load('resources/sounds/mixkit-game-level-music-689.wav')
pygame.mixer.music.load('resources/sounds/mixkit-game-ball-tap-2073.wav', 'ate')
pygame.mixer.Channel(0).play(pygame.mixer.Sound('resources/sounds/mixkit-game-level-music-689.wav'), -1)


class Game:
    def __init__(self):
        self.__x = width/2
        self.__y = height/2 + 8
        self.__snake_body = [(width / 2, height / 2 + 8, 0), (width / 2, height / 2 + 24, 0), (width / 2, height / 2 + 40, 0)]
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
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP and old_direction != 'down':
                    self.__direction = "up"
                    if old_direction != self.__direction:
                        self.__event = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN and old_direction != 'up':
                    self.__direction = "down"
                    if old_direction != self.__direction:
                        self.__event = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT and old_direction != 'right':
                    self.__direction = "left"
                    if old_direction != self.__direction:
                        self.__event = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and old_direction != 'left':
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
            if self.__y == 0:
                self.__y = height - 16
            else:
                self.__y -= tile_size
        elif direction == "down":
            if self.__y == height - 16:
                self.__y = 0
            else:
                self.__y += tile_size
        elif direction == "left":
            if self.__x == 0:
                self.__x = width - 16
            else:
                self.__x -= tile_size
        elif direction == "right":
            if self.__x == width - 16:
                self.__x = 0
            else:
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
            rotate = 0
            if self.__direction == 'up':
                rotate = 0
            elif self.__direction == 'down':
                rotate = 180
            elif self.__direction == 'right':
                rotate = 270
            elif self.__direction == 'left':
                rotate = 90
            new_body[0] = (self.__x, self.__y, rotate)
            new_body[1:] = self.__snake_body[0:-1]
            self.__snake_body = new_body

        head_rect = pygame.Rect(self.__snake_body[0][0], self.__snake_body[0][1], tile_size, tile_size)
        screen.blit(pygame.transform.rotate(snake_head, self.__snake_body[0][2]), head_rect)

        for body in self.__snake_body[1:-1]:
            body_rect = pygame.Rect(body[0], body[1], tile_size, tile_size)
            pygame.draw.rect(screen, (255, 0, 0), body_rect)
            screen.blit(pygame.transform.rotate(snake_body, body[2]), body_rect)

        tail_rect = pygame.Rect(self.__snake_body[-1][0], self.__snake_body[-1][1], tile_size, tile_size)
        screen.blit(pygame.transform.rotate(snake_tail, self.__snake_body[-1][2]), tail_rect)


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
