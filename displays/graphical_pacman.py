import sys

from mechanics import layout


class PacmanDisplay():
    def initialize(self, the_board):
        pass


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print("Graphical Pac-Man display requires Python 3.x.")
        sys.exit(1)

    # TRYING TO GET THIS COMMAND TO WORK.
    # Requires layout, from mechanics
    # How do you go back a directory to import something?

    board = layout.get_layout("test_maze.lay")
    display = PacmanDisplay()
    display.initialize(board)
