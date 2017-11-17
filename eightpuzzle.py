import sys
import random

import agents_search
import search


class EightPuzzleState:
    """
    This class defines the mechanics of the Eight Puzzle. The task of
    recasting this puzzle as a search problem is left to the class
    called EightPuzzleSearchProblem.
    """
    def __init__(self, numbers):
        """
        Constructs a new eight puzzle from an ordering of numbers. If given
        this list:

        [1, 0, 2, 3, 4, 5, 6, 7, 8]

        The representation of the eight puzzle will be:

        -------------
        | 1 |   | 2 |
        -------------
        | 3 | 4 | 5 |
        -------------
        | 6 | 7 | 8 |
        -------------

        The configuration of the puzzle is stored in a two-dimensional list
        (a list of lists) called 'cells'.

        :param numbers: a list of integers from 0 to 8 representing an
        instance of the eight puzzle. 0 represents the blank space.
        """
        self.cells = []

        # A copy is made of the passed in numbers so as not to cause any
        # side effects.
        numbers = numbers[:]
        numbers.reverse()

        for row in range(3):
            self.cells.append([])
            for col in range(3):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blank_location = row, col

    def result(self, move):
        """
        Returns a new eight puzzle with the current state and blank location
        updated based on the provided move.

        The move should be a string drawn from a list returned by legal_moves.
        Illegal moves will raise an exception.

        This function *does not* change the current object. Instead, it will
        return a new object.

        :param move: the move to apply to the current eight puzzle instance
        :return: modified eight puzzle instance based on move applied
        """
        row, col = self.blank_location

        if move == 'up':
            new_row = row - 1
            new_col = col
        elif move == 'down':
            new_row = row + 1
            new_col = col
        elif move == 'left':
            new_row = row
            new_col = col - 1
        elif move == 'right':
            new_row = row
            new_col = col + 1
        else:
            raise Exception("Illegal Move")

        # Create a copy of the current eight puzzle.
        new_puzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        new_puzzle.cells = [values[:] for values in self.cells]

        # Update the copy to reflect the move applied.
        new_puzzle.cells[row][col] = self.cells[new_row][new_col]
        new_puzzle.cells[new_row][new_col] = self.cells[row][col]
        new_puzzle.blank_location = new_row, new_col

        return new_puzzle

    def legal_moves(self):
        """
        Returns a list of legal moves from the current eight puzzle state.

        Moves consist of moving the blank location up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right', respectively.

        For example, this call:

        EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legal_moves()

        Would return:

        ['down', 'right']

        :return: array of legal moves for the blank location
        """
        moves = []
        row, col = self.blank_location

        if row != 0:
            moves.append('up')
        if row != 2:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 2:
            moves.append('right')

        return moves

    def is_goal(self):
        """
        Checks to see if the puzzle is in its goal state. The goal state for
        an eight puzzle is as follows:

        -------------
        |   | 1 | 2 |
        -------------
        | 3 | 4 | 5 |
        -------------
        | 6 | 7 | 8 |
        -------------

        That would be represented as such:

        EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).is_goal()

        would return True.

        An example like this:

        EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).is_goal()

        would return False.

        :return: boolean indicating if goal state is achieved
        """
        current = 0
        for row in range(3):
            for col in range(3):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def __get_ascii_repr(self):
        """
        Provides an ASCII representation for an eight puzzle maze.
        """
        lines = []
        horizontal_line = ('-' * 13)
        lines.append(horizontal_line)

        for row in self.cells:
            row_line = '|'

            for col in row:
                if col == 0:
                    col = ' '
                row_line = row_line + ' ' + col.__str__() + ' |'

            lines.append(row_line)
            lines.append(horizontal_line)

        return '\n'.join(lines)

    def __str__(self):
        return self.__get_ascii_repr()

    def __eq__(self, other):
        """
        Overloads '==' such that two eightPuzzles with the same configuration
        are equal. For example, consider these puzzles:

        puzzle_01 = EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8])
        puzzle_02 = EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8])
        puzzle_change = puzzle_02.result('left')
        print(puzzle_01 == puzzle_change)


         == EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left'))

        :param other: the instance to compare with
        :return: True or False depending on equality
        """
        for row in range(3):
            if self.cells[row] != other.cells[row]:
                return False

        return True

    def __hash__(self):
        return hash(str(self.cells))


class EightPuzzleSearchProblem(agents_search.SearchProblem):
    """
    Implementation of a SearchProblem for the Eight Puzzle domain of problems.

    Each state is represented by an instance of an eight puzzle.

    Each successor is either left, right, up, or down from the original state.
    There is a cost of 1.0 for each move.
    """
    def __init__(self, the_puzzle):
        self.puzzle = the_puzzle

    def get_start_state(self):
        return puzzle

    def is_goal_state(self, state):
        return state.is_goal()

    def get_successors(self, state):
        successor = []

        for move in state.legal_moves():
            successor.append((state.result(move), move, 1))

        return successor

    def get_cost_of_actions(self, actions):
        return len(actions)


def create_random_eight_puzzle(moves=100):
    """
    Creates a random eight puzzle by applying a series of 'moves',
    which are random moves to a solved puzzle.
    :param moves: number of random moves to apply
    :return: puzzle instance
    """
    eight_puzzle = EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8])

    for move in range(moves):
        # Execute a random legal move.
        eight_puzzle = eight_puzzle.result(random.sample(eight_puzzle.legal_moves(), 1)[0])

    return eight_puzzle


EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]


def load_eight_puzzle(puzzle_number):
    """
    Returns an eight puzzle object generated from one of the provided
    puzzles in the EIGHT_PUZZLE_DATA array. The puzzle number can be
    in the range of 0 to 5.

    For example, this:

    print(load_eight_puzzle(0))

    would produce:

    -------------
    | 1 |   | 2 |
    -------------
    | 3 | 4 | 5 |
    -------------
    | 6 | 7 | 8 |
    -------------

    :param puzzle_number: the number of the eight puzzle to load
    :return: an eight puzzle instance
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzle_number])


def step_by_step(the_puzzle, the_path):
    current_step = the_puzzle
    step = 1

    for a in the_path:
        current_step = current_step.result(a)
        print('After %d move%s: %s' % (step, ("", "s")[step > 1], a))
        print(current_step)

        input("Press return for the next state...")
        step += 1


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print("EightPuzzle requires Python 3.x.")
        sys.exit(1)

    puzzle = create_random_eight_puzzle(25)
    print("A Random Puzzle:")
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle)

    path = search.breadth_first_search(problem)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))

    # path = search.depth_first_search(problem)
    # print('DFS found a path of %d moves: %s' % (len(path), str(path)))

    # path = search.uniform_cost_search(problem)
    # print('UCS found a path of %d moves: %s' % (len(path), str(path)))

    # path = search.astar_search(problem)
    # print('A* found a path of %d moves: %s' % (len(path), str(path)))

    step_by_step(puzzle, path)
