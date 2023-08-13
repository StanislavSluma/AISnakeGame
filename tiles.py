import os, csv


class TileSet:
    def __init__(self, file, size=(16,16), margin=0, padding=0):
        pass


class TileMap:
    def __init__(self):
        pass

    def read_csv(self, filename):
        tile_map = []
        with open(os.path.join(filename)) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                tile_map.append(list(row))
                print(list(row))
        return tile_map

    def draw_map(self, surface):
        pass



