import time

from game import Game
from tiles import *
from config import *


if __name__ == '__main__':
    tm = TileMap()
    tm.read_csv('resources/level_design/snakeLevel.csv')
    tm.draw_map(screen)
    game = Game()
    pygame.display.update()
    global running
    while running:
        score, is_over = game.event_listener()
        if is_over:
            game.game_over()
            break
    time.sleep(2.8)
    pygame.quit()
