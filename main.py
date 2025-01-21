from game import Game
from config import *


if __name__ == '__main__':
    game = Game()
    res = game.game_menu()
    pygame.display.update()
    global running
    episode = 1
    total_reward = 0
    step = 1
    while running:
        if res == 'game':
            is_over = game.event_listener()
        elif res == 'bot':
            is_over = game.with_bot()
        elif res == 'agent':
            is_over, total_reward, step = game.agent_training(total_reward, step)
        else:
            sys.exit()
        if is_over:
            # should_continue = game.game_over()
            # if not should_continue:
            #     running = False
            #     break
            # else:
            print(f"episode: {episode}")
            print(f"agent_total_reward: {total_reward}")
            total_reward = 0
            episode += 1
            if episode in [500, 1000, 2000, 4000, 6000, 8000, 10000, 20000, 30000, 40000, 50000]:
                game.save_agent(episode)
            game.new_game()
    sys.exit()
