import pygame.display
import pygame.event
import pygame.font
import pygame.image
import pygame.mixer
import pygame.time

from config import screen, dict_keys_unkeys, width, height
from food import Food
from snake import Snake


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('resources/sounds/mixkit-game-level-music-689.wav')
        pygame.mixer.music.load('resources/sounds/laxity-crosswords-by-seraphic-music.mp3')
        pygame.mixer.music.load('resources/sounds/mixkit-game-ball-tap-2073.wav')
        pygame.mixer.music.load('resources/sounds/mixkit-player-losing-or-failing-2042.wav')
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('resources/sounds/mixkit-game-level-music-689.wav'), -1)
        self.bg()
        self.__snake = Snake()
        self.__food = Food()
        self.__score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""

    def bg(self):
        background = pygame.image.load('resources/level_design/snakeBg.png')
        screen.blit(background, (0, 0))

    def event_listener(self):
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
            if event.type == pygame.KEYDOWN and event.key in dict_keys_unkeys and self.__event:
                if old_direction != dict_keys_unkeys[event.key][1]:
                    self.__event = False
                    self.__direction = dict_keys_unkeys[event.key][0]
        self.__event = True
        self.__snake.move(self.__direction)
        self.__check_for_food()
        self.__snake.draw_snake(self.__direction, self.bg)
        game_over = self.__snake.is_collision()
        self.__food.place_food()
        self.clock.tick(self.__snake.speed)
        pygame.display.update()
        return self.__score, game_over

    def __check_for_food(self):
        if self.__snake.get_place_head() == self.__food.get_food_point():
            self.__food.food = False
            self.__score += 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('resources/sounds/mixkit-game-ball-tap-2073.wav'))
            pygame.display.set_caption(f"Snake game Score : {self.__score}")
            self.__snake.speed = 8 + self.__score // 8
            self.__snake.ate()

    def game_over(self):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound('resources/sounds/mixkit-player-losing-or-failing-2042.wav'), -1
        )
        screen.fill(pygame.Color('black'))
        font = pygame.font.SysFont('chalkduster.ttf', 72)
        game_over = 'GAME OVER'
        your_score = f'YOUR SCORE {self.__score}'
        text1 = font.render(game_over, True, pygame.Color('red'))
        text2 = font.render(your_score, True, pygame.Color('green'))
        screen.blit(text1, (width/2 - 200, height/2 - 100))
        screen.blit(text2, (width/2 - 200, height/2))
        pygame.display.update()
