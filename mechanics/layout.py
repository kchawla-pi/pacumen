import os
import sys
import random
from mechanics.grid import Grid


class Layout:
    def __init__(self, layout_text):
        self.layout_text = layout_text
        self.width = len(layout_text[0])
        self.height = len(layout_text)
        self.walls = Grid(self.width, self.height, False)
        self.dots = Grid(self.width, self.height, False)
        self.agent_positions = []
        self.process_layout_text(layout_text)
        self.total_dots = len(self.dots.as_list())

    def __str__(self):
        return "\n".join(self.layout_text)

    def process_layout_text(self, layout_text):
        maximum_y = self.height - 1

        for y in range(self.height):
            for x in range(self.width):
                layout_char = layout_text[maximum_y - y][x]
                self.process_layout_character(x, y, layout_char)

    def process_layout_character(self, x, y, layout_character):
        if layout_character == '%':
            self.walls[x][y] = True
        elif layout_character == '.':
            self.dots[x][y] = True
        elif layout_character == 'P':
            self.agent_positions.append((0, (x, y)))

    def is_wall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def get_random_legal_position(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))

        while self.is_wall((x, y)):
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))

        return x, y

    def get_random_corner(self):
        possibles = [(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        return random.choice(possibles)


def get_layout(name, back=1):
    if name.endswith('.lay'):
        layout = load_layout('layouts/' + name)
        if layout is None:
            layout = load_layout(name)
    else:
        layout = load_layout('layouts/' + name + '.lay')
        if layout is None:
            layout = load_layout(name + '.lay')

    if layout is None and back >= 0:
        current_directory = os.path.abspath('.')
        os.chdir('..')
        layout = get_layout(name, back - 1)
        os.chdir(current_directory)

    return layout


def load_layout(fullname):
    if not os.path.exists(fullname):
        return None

    f = open(fullname)

    try:
        return Layout([line.strip() for line in f])
    finally:
        f.close()


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print("Layout requires Python 3.x.")
        sys.exit(1)

    game_layout = get_layout("test_maze")
    print("Width:", game_layout.width)
    print("Height:", game_layout.height)
    print("Walls:\n{}".format(game_layout.walls))
    print("Dots:\n{}".format(game_layout.dots))
    print("Total Dots:", game_layout.total_dots)
    print("Dot Locations:", game_layout.dots.as_list())
    print("Agent Positions:", game_layout.agent_positions)
    print("Is 2,1 a wall?", game_layout.is_wall((2, 1)))
    print("Is 3,1 a wall?", game_layout.is_wall((3, 1)))
    print("Random legal position:", game_layout.get_random_legal_position())
    print("Random legal corner:", game_layout.get_random_corner())
