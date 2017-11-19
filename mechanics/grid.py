class Grid:
    def __init__(self, width, height, initial_value=False):
        self.width = width
        self.height = height
        self.data = [[initial_value for _ in range(height)] for _ in range(width)]

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __getitem__(self, i):
        return self.data[i]

    def as_list(self):
        grid_list = []

        for x in range(self.width):
            for y in range(self.height):
                if self[x][y]:
                    grid_list.append((x, y))

        return grid_list
