import sys

from game import Game, Button
from config import *


if __name__ == '__main__':
    game = Game()
    game.game_menu()
    pygame.display.update()
    global running
    global game_over
    while running:
        is_over = game.event_listener()
        if is_over:
            should_continue = game.game_over()
            if not should_continue:
                running = False
                break
            else:
                game.new_game()
    pygame.quit()
    sys.exit()
