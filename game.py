import sys

import pygame.display
import pygame.event
import pygame.font
import pygame.image
import pygame.mixer
import pygame.time
import shelve

from config import screen, dict_keys_unkeys, width, height, menu_image
from food import Food
from snake import Snake
from tiles import TileMap
from button import Button


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load('resources/sounds/mixkit-game-level-music-689.wav')
        pygame.mixer.music.load('resources/sounds/laxity-crosswords-by-seraphic-music.mp3')
        pygame.mixer.music.load('resources/sounds/mixkit-game-ball-tap-2073.wav')
        pygame.mixer.music.load('resources/sounds/mixkit-player-losing-or-failing-2042.wav')
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('resources/sounds/mixkit-game-level-music-689.wav'), -1)
        self.__tile_map = TileMap()
        self.__tile_map.read_csv('resources/level_design/snakeLevel.csv')
        self.__sur = pygame.Surface((width, height))
        self._sur = self.__tile_map.draw_map(self.__sur)
        self.__snake = Snake()
        self.__food = [Food(), Food(), Food()]
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body)
        self.__score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""
        self.__save_best_score()

    def event_listener(self):
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in dict_keys_unkeys and self.__event:
                if self.__direction != '' or (event.key != pygame.K_s and event.key != pygame.K_DOWN):
                    if old_direction != dict_keys_unkeys[event.key][1]:
                        self.__event = False
                        self.__direction = dict_keys_unkeys[event.key][0]
        self.__event = True
        self.__snake.move(self.__direction)
        self.__check_for_food()
        screen.blit(self.__sur, (0, 0))
        self.__snake.draw_snake(self.__direction)
        global game_over
        game_over = self.__snake.is_collision(self.__tile_map.rock_coordinates)
        self.__snake.is_in_bush(self.__tile_map.bush_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body)
        self.clock.tick(self.__snake.speed)
        pygame.display.update()
        return game_over

    def __check_for_food(self):
        for food in self.__food:
            if self.__snake.get_place_head() == food.get_food_point():
                food.food = False
                if food.type_food == 'apple':
                    self.__score += 1
                else:
                    self.__score += 3
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('resources/sounds/mixkit-game-ball-tap-2073.wav'))
                pygame.display.set_caption(f"Snake game Score : {self.__score}")
                if self.__score % 8 == 0:
                    self.__snake.ate(1, food.type_food)
                else:
                    self.__snake.ate(0, food.type_food)

    def game_over(self):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound('resources/sounds/mixkit-player-losing-or-failing-2042.wav')
        )
        self.__save_best_score()
        screen.fill(pygame.Color('black'))
        font = pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 72)
        game_over = '  GAME OVER'
        your_score = f'YOUR SCORE {self.__score}'
        your_best_score = f'YOUR BEST SCORE {self.__get_best_score()}'
        font2 = pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 22)
        key_to_continue = 'PRESS P TO PLAY AGAIN OR E TO EXIT'
        text1 = font.render(game_over, True, pygame.Color('red'))
        text2 = font.render(your_score, True, pygame.Color('green'))
        text3 = font2.render(key_to_continue, True, pygame.Color('white'))
        text4 = font2.render(your_best_score, True, pygame.Color('white'))
        screen.blit(text1, (width/2 - text1.get_width()/2, height/2 - 100))
        screen.blit(text2, (width/2 - text2.get_width()/2, height/2))
        screen.blit(text3, (width/2 - text3.get_width()/2, height/2 + 100))
        screen.blit(text4, (width/2 - text4.get_width()/2, height/2 + 200))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return True
                    elif event.key == pygame.K_e:
                        return False

    def new_game(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('resources/sounds/mixkit-game-level-music-689.wav'), -1)
        self._sur = self.__tile_map.generate_tile_map(self.__sur)
        screen.blit(self.__sur, (0, 0))
        self.__snake = Snake()
        self.__food = [Food(), Food(), Food()]
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body)
        self.__score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""
        pygame.display.set_caption(f"Snake game Score : 0")
        pygame.display.update()

    def game_menu(self):
        pygame.mixer.Channel(4).play(
            pygame.mixer.Sound('resources/sounds/laxity-crosswords-by-seraphic-music.mp3'), -1
        )
        pygame.display.set_caption('Menu')
        menu_running = True
        screen.blit(menu_image, (0, 0))
        font = pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 30)
        score = self.__get_best_score()
        best_score = font.render(f'YOUR BEST SCORE {score}', True, pygame.Color('green'))
        screen.blit(best_score, (width / 2 - best_score.get_width()/2, 160))
        play_button = Button((width / 2, height / 2), 'PLAY',
                             pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 32),
                             pygame.Color('green'), screen)
        quit_button = Button((width / 2, height / 2 + 100),  'QUIT',
                             pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 32), pygame.Color('red'),
                             screen)
        while menu_running:
            mouse_pos = pygame.mouse.get_pos()
            for button in [play_button, quit_button]:
                button.change_color(mouse_pos)
                button.update()
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_input(mouse_pos):
                        pygame.display.set_caption('Snake game')
                        menu_running = False
                        pygame.mixer.Channel(4).pause()
                        break
                    if quit_button.check_input(mouse_pos):
                        pygame.quit()

    def __save_best_score(self):
        with (shelve.open('resources/score.txt')) as score:
            old_score = self.__get_best_score()
            if self.__score > old_score:
                score['best_score'] = self.__score
                score.close()

    def __get_best_score(self):
        with (shelve.open('resources/score.txt')) as score:
            score_ = score['best_score']
            score.close()
            return score_
