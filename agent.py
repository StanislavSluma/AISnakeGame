import torch
from config import width, height, tile_size
from snake import Snake


class Agent(Snake):
    def __init__(self, x, y, alpha=0.1, gamma=1.):
        super().__init__()
        self.direction = 'up'
        self.undirect = {'up': 'down', 'down': 'up', 'right': 'left', 'left': 'right'}
        self._x = int(x)
        self._y = int(y)
        self._snake_body = [
            [x, y, 0], [x, y + 16, 0], [x, y + 32, 0]
        ]
        self._new_snake_coordinates = []

        self.dqn = torch.nn.Sequential(
            torch.nn.Linear(31*62, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 4)
        )
        # self.dqn = torch.nn.Sequential(
        #     # 62*31
        #     torch.nn.Conv2d(1, 8, 3),
        #     # 60*29
        #     torch.nn.ReLU(),
        #     torch.nn.MaxPool2d(2, 2),
        #     # 30*14
        #     torch.nn.Conv2d(8, 16, 3),
        #     # 28*12
        #     torch.nn.ReLU(),
        #     torch.nn.MaxPool2d(2, 2),
        #     # 14*6
        #     torch.nn.Flatten(),
        #     # 14*16*6
        #     torch.nn.Linear(16*14*6, 256),
        #     torch.nn.ReLU(),
        #     torch.nn.Linear(256, 4)
        # )
        # self.dqn = torch.load("0_episodes", weights_only=False)
        self.optim = torch.optim.Adam(self.dqn.parameters())
        self.loss = torch.nn.MSELoss()
        self.alpha = alpha
        self.gamma = gamma

    def get_dqn(self):
        return self.dqn

    def set_dqn(self, dqn):
        self.dqn = dqn
        self.optim = torch.optim.Adam(self.dqn.parameters())

    def __align(self, food_coordinates, block_coordinates):
        self.__new_food_coordinates = []
        self.__new_block_coordinates = []
        self.__new_snake_coordinates = []
        snake_body = self.snake_body_xy()
        delta_x = int(round(width / tile_size / 2) - snake_body[0][0] / tile_size)
        delta_y = int(round(height / tile_size / 2) - snake_body[0][1] / tile_size)
        for food_point in food_coordinates:
            food_x = int((food_point[0] / tile_size + delta_x + width / tile_size) % (width / tile_size))
            food_y = int((food_point[1] / tile_size + delta_y + height / tile_size) % (height / tile_size))
            self.__new_food_coordinates.append([food_x, food_y])
        for block_point in block_coordinates:
            temp = int((int(block_point[0]) / tile_size + delta_x + width / tile_size))
            block_x = int(temp % (width / tile_size))
            temp = int((int(block_point[1]) / tile_size + delta_y + height / tile_size))
            block_y = int(temp % (height / tile_size))
            self.__new_block_coordinates.append([block_x, block_y])
        for snake_part in snake_body[1:]:
            temp = int((int(snake_part[0]) / tile_size + delta_x + width / tile_size))
            block_x = int(temp % (width / tile_size))
            temp = int((int(snake_part[1]) / tile_size + delta_y + height / tile_size))
            block_y = int(temp % (height / tile_size))
            self.__new_snake_coordinates.append([block_x, block_y])

    def to_state(self, food_coordinates, block_coordinates):
        # agent_map_s = torch.zeros(62, 31)
        # agent_map_f = torch.zeros(62, 31)
        # agent_map_b = torch.zeros(62, 31)
        # self.__align(food_coordinates, block_coordinates)
        # for x, y in self.__new_snake_coordinates:
        #     agent_map_s[x][y] = 1
        # for x, y in self.__new_food_coordinates:
        #     agent_map_f[x][y] = 1
        # for x, y in self.__new_block_coordinates:
        #     agent_map_b[x][y] = 1
        # return torch.cat((agent_map_s.reshape(31*62), agent_map_f.reshape(31*62), agent_map_b.reshape(31*62)), 0)
        agent_map = torch.zeros(62, 31)
        self.__align(food_coordinates, block_coordinates)
        for x, y in self.__new_snake_coordinates:
            agent_map[x][y] = -1
        for x, y in self.__new_food_coordinates:
            agent_map[x][y] = 1
        for x, y in self.__new_block_coordinates:
            agent_map[x][y] = -1
        return agent_map.reshape(62*31)
        # agent_map = torch.zeros(62, 31)
        # self.__align(food_coordinates, block_coordinates)
        # for x, y in self.__new_snake_coordinates:
        #     agent_map[x][y] = -10
        # for x, y in self.__new_food_coordinates:
        #     agent_map[x][y] = 10
        # for x, y in self.__new_block_coordinates:
        #     agent_map[x][y] = -20
        # return agent_map.reshape([1, 1, 62, 31])

    def save(self, episode):
        torch.save(self.dqn, f"{episode}_episodes")

    def make_decision(self, state, eps=0.):
        new_direction = self.undirect[self.direction]
        with torch.no_grad():
            directions = ['up', 'down', 'left', 'right']
            if torch.rand((1,)).item() > eps:
                action = torch.argmax(self.dqn(state)).item()
            else:
                while new_direction == self.undirect[self.direction]:
                    action = torch.randint(0, 4, (1,)).item()
                    new_direction = directions[action]
            self.direction = directions[action]
            return directions[action], action

    def update(self, state, next_state, action, reward, gamma=1.0):
        self.optim.zero_grad()

        q_values = self.dqn(state)
        # print(f"q_values: {q_values}")
        # print(f"state: {state[31][16]}")
        q_values_next = self.dqn(next_state).detach()
        # print(f"q_values_next: {q_values_next}")
        # print(f"next_state: {next_state[31][16]}")

        q_values_should_be = q_values.tolist().copy()
        # print(f"action {action}")
        q_values_should_be[action] = reward + gamma * torch.max(q_values_next).item()
        # print(f"q_values_should_be: {q_values_should_be}")

        loss = self.loss(q_values, torch.Tensor(q_values_should_be))
        # print(f"loss: {loss.item()}")
        loss.backward()
        self.optim.step()
