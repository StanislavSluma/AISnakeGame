import sys
import os

import pygame.display
import pygame.event
import pygame.font
import pygame.image
import pygame.mixer
import pygame.time
import shelve

from config import screen, dict_keys_unkeys, width, height, menu_image, resource_path, tile329
from food import Food
from snake import Snake
from snake_bot import SnakeBot
from agent import Agent
from tiles import TileMap
from button import Button


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.music.load(resource_path(os.path.join('resources/sounds', 'mixkit-game-level-music-689.wav')))
        pygame.mixer.music.load(resource_path(os.path.join('resources/sounds', 'laxity-crosswords-by-seraphic-music.mp3')))
        pygame.mixer.music.load(resource_path(os.path.join('resources/sounds', 'mixkit-game-ball-tap-2073.wav')))
        pygame.mixer.music.load(resource_path(os.path.join('resources/sounds', 'mixkit-player-losing-or-failing-2042.wav')))
        pygame.mixer.music.load(resource_path(os.path.join('resources/sounds', 'mixkit-winning-an-extra-bonus-2060.wav')))
        self.__tile_map = TileMap()
        self.__tile_map.read_csv(resource_path(os.path.join('resources/level_design', 'snakeLevel.csv')))
        self.__sur = pygame.Surface((width, height))
        self._sur = self.__tile_map.draw_map(self.__sur)
        self.__snake = Snake()
        self.__bot_snake = SnakeBot(width / 2 + 32, height / 2 + 8)
        self.__agent = Agent(width // 2, height // 2 + 8)
        self.__food_amount = 10
        self.__food = [Food() for _ in range(self.__food_amount)]
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body)
        self.__score = 0
        self.__bot_score = 0
        self.__agent_score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""
        self.__save_best_score()

    def with_bot(self):
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in dict_keys_unkeys and self.__event:
                if self.__direction != '' or (event.key != pygame.K_s and event.key != pygame.K_DOWN):
                    if old_direction != dict_keys_unkeys[event.key][1]:
                        self.__event = False
                        self.__direction = dict_keys_unkeys[event.key][0]
        self.__event = True

        food_coordinates, block_coordinates = self.__bot_map()
        block_coordinates += self.__snake.snake_body_xy()
        bot_direction = self.__bot_snake.decide_direction(food_coordinates, block_coordinates)

        self.__snake.move(self.__direction)
        self.__bot_snake.move(bot_direction)
        self.__check_for_food()
        self.__check_for_food_ml()
        screen.blit(self.__sur, (0, 0))
        self.__snake.draw_snake(self.__direction)
        self.__bot_snake.draw_snake(bot_direction)

        game_over = self.__snake.is_collision(self.__tile_map.rock_coordinates + self.__bot_snake.snake_body_xy())
        if self.__bot_snake.is_collision(self.__tile_map.rock_coordinates + self.__snake.snake_body_xy()):
            self.__turn_to_rocks()

        self.__snake.is_in_bush(self.__tile_map.bush_coordinates)
        self.__bot_snake.is_in_bush(self.__tile_map.bush_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body_xy() + self.__bot_snake.snake_body_xy())
        self.clock.tick(8)
        pygame.display.update()
        return game_over

    def with_agent(self):
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in dict_keys_unkeys and self.__event:
                if self.__direction != '' or (event.key != pygame.K_s and event.key != pygame.K_DOWN):
                    if old_direction != dict_keys_unkeys[event.key][1]:
                        self.__event = False
                        self.__direction = dict_keys_unkeys[event.key][0]
        self.__event = True

        food_coordinates, block_coordinates = self.__bot_map()
        block_coordinates += self.__snake.snake_body_xy()
        bot_direction = self.__bot_snake.decide_direction(food_coordinates, block_coordinates)

        self.__snake.move(self.__direction)
        self.__bot_snake.move(bot_direction)
        self.__check_for_food()
        self.__check_for_food_ml()
        screen.blit(self.__sur, (0, 0))
        self.__snake.draw_snake(self.__direction)
        self.__bot_snake.draw_snake(bot_direction)

        game_over = self.__snake.is_collision(self.__tile_map.rock_coordinates + self.__bot_snake.snake_body_xy())
        if self.__bot_snake.is_collision(self.__tile_map.rock_coordinates + self.__snake.snake_body_xy()):
            self.__turn_to_rocks()

        self.__snake.is_in_bush(self.__tile_map.bush_coordinates)
        self.__bot_snake.is_in_bush(self.__tile_map.bush_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body_xy() + self.__bot_snake.snake_body_xy())
        self.clock.tick(8)
        pygame.display.update()
        return game_over

    def agent_training(self, total_reward, step):
        food_coord, block_coord = self.__agent_map()
        state = self.__agent.to_state(food_coord, block_coord)
        agent_direction, action = self.__agent.make_decision(state, 0.05)

        self.__agent.move(agent_direction)
        is_ate_food = self.__check_for_food_rl()
        screen.blit(self.__sur, (0, 0))
        self.__agent.draw_snake(agent_direction)
        game_over = self.__agent.is_collision(self.__tile_map.rock_coordinates)
        self.__agent.is_in_bush(self.__tile_map.bush_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__agent.snake_body_xy())
        # self.clock.tick(self.__agent.speed)
        pygame.display.update()

        step += 1
        reward = 0.1
        if game_over:
            #reward = -100 / (step ** 1/2)
            reward = -1
            step = 1
            print(f"agent_score: {self.__agent_score}")
        if is_ate_food:
            #reward = step ** 1/2
            reward = 1

        total_reward += reward
        food_coord, block_coord = self.__agent_map()
        next_state = self.__agent.to_state(food_coord, block_coord)
        self.__agent.update(state, next_state, action, reward, gamma=1.)

        return game_over, total_reward, step

    def save_agent(self, episode):
        self.__agent.save(episode)

    def event_listener(self):
        for event in pygame.event.get():
            old_direction = self.__direction
            if event.type == pygame.QUIT:
                global running
                running = False
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
        game_over = self.__snake.is_collision(self.__tile_map.rock_coordinates)
        self.__snake.is_in_bush(self.__tile_map.bush_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body_xy())
        self.clock.tick(self.__snake.speed)
        pygame.display.update()
        return game_over

    def machine_learning(self):

        food_coord, block_coord = self.__bot_map()
        bot_direction = self.__bot_snake.decide_direction(food_coord, block_coord)
        #self.__direction = bot_direction

        '''
        if self.__event == True:
            print(f'Bot Direction: {bot_direction}')
            self.__event = False
        '''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.__direction = dict_keys_unkeys[event.key][0]
                self.__event = True
        
        self.__bot_snake.learning(bot_direction, self.__direction)

        self.__bot_snake.move(self.__direction)
        self.__check_for_food_ml()
        screen.blit(self.__sur, (0, 0))
        self.__bot_snake.draw_snake(self.__direction)
        game_over = self.__bot_snake.is_collision(self.__tile_map.rock_coordinates)
        self.__bot_snake.is_in_bush(self.__tile_map.bush_coordinates)
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__bot_snake.snake_body_xy())
        self.clock.tick(self.__bot_snake.speed)
        pygame.display.update()
        self.__direction = ""
        return game_over

    def __check_for_food(self):
        for food in self.__food:
            if self.__snake.get_place_head() == food.get_food_point():
                food.food = False
                if food.type_food == 'apple':
                    self.__score += 1
                else:
                    self.__score += 3
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(resource_path(os.path.join('resources/sounds', 'mixkit-game-ball-tap-2073.wav'))))
                pygame.display.set_caption(f"Snake game Your Score : {self.__score}    Bot Score : {self.__bot_score}")
                if self.__score % 8 == 0:
                    self.__snake.ate(1, food.type_food)
                else:
                    self.__snake.ate(0, food.type_food)

    def __check_for_food_ml(self):
        for food in self.__food:
            if self.__bot_snake.get_place_head() == food.get_food_point():
                food.food = False
                if food.type_food == 'apple':
                    self.__bot_score += 1
                else:
                    self.__bot_score += 3
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(resource_path(os.path.join('resources/sounds', 'mixkit-game-ball-tap-2073.wav'))))
                pygame.display.set_caption(f"Snake game Your Score : {self.__score}    Bot Score : {self.__bot_score}")
                if self.__score % 8 == 0:
                    self.__bot_snake.ate(1, food.type_food)
                else:
                    self.__bot_snake.ate(0, food.type_food)

    def __check_for_food_rl(self):
        head = self.__agent.get_place_head()
        for food in self.__food:
            food_xy = food.get_food_point()
            if head[0] == food_xy[0] and head[1] == food_xy[1]:
                food.food = False
                if food.type_food == 'apple':
                    self.__agent_score += 1
                else:
                    self.__agent_score += 3
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(resource_path(os.path.join('resources/sounds', 'mixkit-game-ball-tap-2073.wav'))))
                pygame.display.set_caption(f"Snake game Your Score : {self.__score}    Bot Score : {self.__agent_score}")
                if self.__score % 8 == 0:
                    self.__agent.ate(1, food.type_food)
                else:
                    self.__agent.ate(0, food.type_food)
                return True
        return False

    def __bot_map(self):
        food_coordinates = []
        for food in self.__food:
            food_coordinates.append(food.get_food_point())

        snake_coordinates = self.__bot_snake.snake_body_xy()
        snake_coordinates.pop(0)
        block_coordinates = self.__tile_map.rock_coordinates + snake_coordinates
        return food_coordinates, block_coordinates

    def __agent_map(self):
        food_coordinates = []
        for food in self.__food:
            food_coordinates.append(food.get_food_point())
        block_coordinates = self.__tile_map.rock_coordinates.copy()
        return food_coordinates, block_coordinates

    def __turn_to_rocks(self):
        for body in self.__bot_snake.snake_body_xy():
            self.__tile_map.rock_coordinates.append(body)
            self.__sur.blit(tile329, body)

    def game_over(self):
        self.__save_best_score()
        screen.fill(pygame.Color('black'))
        font = pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 72)
        if self.__bot_score == 0 or self.__bot_score > self.__score:
            game_over = '  GAME OVER'
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound(
                    resource_path(os.path.join('resources/sounds', 'mixkit-player-losing-or-failing-2042.wav')))
            )
        else:
            game_over = '   YOU WON '
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound(
                    resource_path(os.path.join('resources/sounds', 'mixkit-winning-an-extra-bonus-2060.wav')))
            )
        your_score = f'YOUR SCORE {self.__score}'
        your_best_score = f'YOUR BEST SCORE {self.__get_best_score()}'
        font2 = pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 22)
        key_to_continue = 'PRESS P TO PLAY AGAIN OR E TO EXIT'
        if game_over == '  GAME OVER':
            text1 = font.render(game_over, True, pygame.Color('red'))
        else:
            text1 = font.render(game_over, True, pygame.Color('blue'))
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
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(resource_path(os.path.join('resources/sounds', 'mixkit-game-level-music-689.wav'))), -1)
        self._sur = self.__tile_map.generate_tile_map(self.__sur)
        screen.blit(self.__sur, (0, 0))
        self.__snake = Snake()
        self.__bot_snake = SnakeBot(width / 2 + 32, height / 2 + 8)
        dqn = self.__agent.get_dqn()
        self.__agent = Agent(width // 2, height // 2 + 8)
        self.__agent.set_dqn(dqn)
        self.__food = [Food() for _ in range(self.__food_amount)]
        for food in self.__food:
            food.place_food(self.__tile_map.rock_coordinates, self.__snake.snake_body)
        self.__score = 0
        self.__bot_score = 0
        self.__agent_score = 0
        self.__event = True
        self.clock = pygame.time.Clock()
        self.__direction = ""
        pygame.display.set_caption(f"Snake game Score : 0")
        pygame.display.update()

    def game_menu(self):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(resource_path(os.path.join('resources/sounds', 'laxity-crosswords-by-seraphic-music.mp3'))), -1
        )
        pygame.display.set_caption('Menu')
        menu_running = True
        screen.blit(menu_image, (0, 0))
        font = pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 17)
        score = self.__get_best_score()
        best_score = font.render(f'YOUR BEST SCORE {score}', True, pygame.Color('blue'))
        screen.blit(best_score, (best_score.get_width()/2 - 120, 30))
        play_button = Button((width / 2, height / 2 + 50), 'Single',
                             pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 32),
                             pygame.Color('green'), screen)
        quit_button = Button((width / 2, height / 2 + 150),  'QUIT',
                             pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 32),
                             pygame.Color('red'), screen)
        bot_button = Button((width / 2, height / 2 - 50),  'With Bot',
                             pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 32),
                             pygame.Color('blue'), screen)
        agent_button = Button((width / 2, height / 2 - 100),  'With Agent',
                             pygame.font.Font(resource_path(os.path.join('resources/fonts', '8-BIT WONDER.TTF')), 32),
                             pygame.Color('blue'), screen)
        while menu_running:
            mouse_pos = pygame.mouse.get_pos()
            for button in [play_button, quit_button, bot_button, agent_button]:
                button.change_color(mouse_pos)
                button.update()
                pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if agent_button.check_input(mouse_pos):
                        pygame.display.set_caption('Snake game')
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
                            resource_path(os.path.join('resources/sounds', 'mixkit-game-level-music-689.wav'))), -1)
                        return 'agent'
                    if bot_button.check_input(mouse_pos):
                        pygame.display.set_caption('Snake game')
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
                            resource_path(os.path.join('resources/sounds', 'mixkit-game-level-music-689.wav'))), -1)
                        return 'bot'
                    if play_button.check_input(mouse_pos):
                        pygame.display.set_caption('Snake game')
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(
                            resource_path(os.path.join('resources/sounds', 'mixkit-game-level-music-689.wav'))), -1)
                        return 'game'
                    if quit_button.check_input(mouse_pos):
                        pygame.display.set_caption('Snake game')
                        return 'quit'

    def __save_best_score(self):
        with (shelve.open(resource_path(os.path.join('resources', 'score.txt')))) as score:
            # score['best_score'] = 0
            old_score = self.__get_best_score()
            if self.__score > old_score:
                score['best_score'] = self.__score
                score.close()

    def __get_best_score(self):
        with (shelve.open(resource_path(os.path.join('resources', 'score.txt')))) as score:
            score_ = score['best_score']
            score.close()
            return score_
