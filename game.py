import pygame.display
import pygame.event
import pygame.font
import pygame.image
import pygame.mixer
import pygame.time

from config import screen, dict_keys_unkeys, width, height
from food import Food
from snake import Snake
from tiles import TileMap


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
            food.place_food(self.__tile_map.tile_coordinates)
        self.__score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""

    def event_listener(self):
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
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
        game_over = self.__snake.is_collision(self.__tile_map.tile_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.tile_coordinates)
        self.clock.tick(self.__snake.speed)
        pygame.display.update()
        return game_over

    def __check_for_food(self):
        for food in self.__food:
            if self.__snake.get_place_head() == food.get_food_point():
                food.food = False
                self.__score += 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('resources/sounds/mixkit-game-ball-tap-2073.wav'))
                pygame.display.set_caption(f"Snake game Score : {self.__score}")
                self.__snake.speed = 8 + self.__score // 8
                self.__snake.ate()

    def game_over(self):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound('resources/sounds/mixkit-player-losing-or-failing-2042.wav')
        )
        screen.fill(pygame.Color('black'))
        font = pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 72)
        game_over = '  GAME OVER'
        your_score = f'YOUR SCORE {self.__score}'
        font2 = pygame.font.Font('resources/fonts/8-BIT WONDER.TTF', 22)
        key_to_continue = 'PRESS P TO PLAY AGAIN OR E TO EXIT'
        text1 = font.render(game_over, True, pygame.Color('red'))
        text2 = font.render(your_score, True, pygame.Color('green'))
        text3 = font2.render(key_to_continue, True, pygame.Color('white'))
        screen.blit(text1, (width/2 - 400, height/2 - 100))
        screen.blit(text2, (width/2 - 400, height/2))
        screen.blit(text3, (width/2 - 300, height/2 + 100))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.__sur = self.__tile_map.generate_tile_map(self.__sur)
                        screen.blit(self.__sur, (0, 0))
                        return True
                    elif event.key == pygame.K_e:
                        return False

    def game_menu(self):
        pass

    def new_game(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('resources/sounds/mixkit-game-level-music-689.wav'), -1)
        self._sur = self.__tile_map.generate_tile_map(self.__sur)
        screen.blit(self.__sur, (0, 0))
        self.__snake = Snake()
        self.__food = [Food(), Food(), Food()]
        for food in self.__food:
            food.place_food(self.__tile_map.tile_coordinates)
        self.__score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""
        pygame.display.update()
