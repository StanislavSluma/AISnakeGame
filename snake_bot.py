from snake import Snake
from config import tile_size, width, height, direction_index, index_direction, os


class SnakeBot(Snake):
    def __init__(self, x, y):
        super().__init__()
        self._x = x
        self._y = y
        self._snake_body = [
            [x, y, 0], [x, y + 16, 0], [x, y + 32, 0]
        ]
        self.__new_food_coordinates = []
        self.__new_block_coordinates = []
        self.__count = 0
        self.__block_map = []
        self.__food_map = []
        i = 0
        while i < 62:
            temp_list = list()
            j = 0
            while j < 31:
                temp_list.append([0, 0, 0, 0])  # direction [up, left, down, right]
                j += 1
            self.__block_map.append(temp_list)
            i += 1
        i = 0
        while i < 62:
            temp_list = list()
            j = 0
            while j < 31:
                temp_list.append([0, 0, 0, 0])  # direction [up, left, down, right]
                j += 1
            self.__food_map.append(temp_list)
            i += 1
        self.__read_brain_map()
        self.__block_map[31][15][0] = -999
        self.__block_map[31][17][2] = -999
        self.__block_map[30][16][1] = -999
        self.__block_map[32][16][3] = -999
        # self.__save_brain_map()

    def __align(self, food_coordinates, block_coordinates):
        self.__new_food_coordinates = []
        self.__new_block_coordinates = []
        delta_x = int(round(width / tile_size / 2) - self._x / tile_size)
        delta_y = int(round(height / tile_size / 2) - self._y / tile_size)
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

    def decide_direction(self, food_coordinates, block_coordinates, event):
        directions = [0, 0, 0, 0]
        self.__align(food_coordinates, block_coordinates)
        for food_point in self.__new_food_coordinates:
            directions[0] += self.__food_map[food_point[0]][food_point[1]][0]
            directions[1] += self.__food_map[food_point[0]][food_point[1]][1]
            directions[2] += self.__food_map[food_point[0]][food_point[1]][2]
            directions[3] += self.__food_map[food_point[0]][food_point[1]][3]
        for block_point in self.__new_block_coordinates:
            directions[0] += self.__block_map[block_point[0]][block_point[1]][0]
            directions[1] += self.__block_map[block_point[0]][block_point[1]][1]
            directions[2] += self.__block_map[block_point[0]][block_point[1]][2]
            directions[3] += self.__block_map[block_point[0]][block_point[1]][3]
        if event == True:

            print(f'up: => {directions[0]}')
            print(f'left: => {directions[1]}')
            print(f'down: => {directions[2]}')
            print(f'right: => {directions[3]}')

        return direction_index[directions.index(max(directions))]

    def learning(self, bot_direction, my_direction):
        if my_direction != "":
            self.__balance(bot_direction, my_direction)

    def __balance(self, bot_direction, my_direction):
        if my_direction != bot_direction:
            print(f"My Direction: {my_direction}")
            for food_point in self.__new_food_coordinates:
                self.__food_map[food_point[0]][food_point[1]][index_direction[my_direction]] += 5
                self.__food_map[food_point[0]][food_point[1]][index_direction[bot_direction]] -= 5
            for block_point in self.__new_block_coordinates:
                self.__block_map[block_point[0]][block_point[1]][index_direction[my_direction]] += 1
                self.__block_map[block_point[0]][block_point[1]][index_direction[bot_direction]] -= 1
            print("Save in FILE")
            self.__save_brain_map()
        else:
            print('CooL!')
            for food_point in self.__new_food_coordinates:
                self.__food_map[food_point[0]][food_point[1]][index_direction[bot_direction]] += 3

    def __save_brain_map(self):
        file = open('bot_map.txt', 'w')
        i = 0
        while i < 62:
            j = 0
            while j < 31:
                k = 0
                while k < 4:
                    file.write(str(self.__food_map[i][j][k]) + ' ')
                    file.write(str(self.__block_map[i][j][k]) + ' ')
                    k += 1
                j += 1
            i += 1
        file.close()

    def __read_brain_map(self):
        file = open('bot_map.txt', 'r')
        temp_list = file.read().split()
        count = 0
        i = 0
        while i < 62:
            j = 0
            while j < 31:
                k = 0
                while k < 4:
                    self.__food_map[i][j][k] = int(temp_list[count])
                    count += 1
                    self.__block_map[i][j][k] = int(temp_list[count])
                    k += 1
                    count += 1
                j += 1
            i += 1
        file.close()
