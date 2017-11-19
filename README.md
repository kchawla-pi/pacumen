## Pacumen

The name of this project is based on the name "Pac-Man" and the word "acumen." The latter term generally refers to the ability to make good judgments and quick decisions. This is often done in a particular domain. That domain, for this project, will be in the context of a Pac-Man game.

That said ...

In the initial commits of this project, you won't see a whole lot of Pac-Man at all. Rather, the basis for testing algorithms of various sorts will be put in place. These will initially be common examples, like the 8 Puzzle, which is a variant of the [15 Puzzle](https://en.wikipedia.org/wiki/15_puzzle).

To that end, **Pacumen** will be an implementation of the [Pacman AI project](http://ai.berkeley.edu) developed at UC Berkeley. In terms of the Berkeley AI code, Pacumen is going to be a substantial change. The most notable is that Pacumen only runs under Python 3.x. Internally, there are going to be a lot of changes as well, in terms of making the code more maintainable and scalable as well as more idiomatic to Python.

### 8 Puzzle

The file [eightpuzzle.py](https://github.com/jeffnyman/pacumen/blob/master/eightpuzzle.py) contains an implementation of an 8 puzzle board representation. Specifically, the entire state of such a puzzle board is encoded as the [EightPuzzleState](https://github.com/jeffnyman/pacumen/blob/master/eightpuzzle.py#L8). The search problem for this board (getting the blank location in the top left) is encoded as the [EightPuzzleSearchProblem](https://github.com/jeffnyman/pacumen/blob/master/eightpuzzle.py#L209).

The nature a search problem, in general, is encoded as a [SearchProblem](https://github.com/jeffnyman/pacumen/blob/master/agents_search.py) The EightPuzzleSearchProblem implements this class and thus must provide methods that are implemented.

The nature of any kind of search problem tends to be relatively generic and the methods that are provided cover the most important aspects.

* get_start_state(): This returns the start state for the search problem. In the case of 8 Puzzle, that means a board with eight numbers and one blank cell.

* is_goal_state(): This returns true is the search problem has been solved, meaning that the current state is a solution. In the case of 8 Puzzle, that means a board where the blank cell is in the top left of the grid.

* get_successors(): A successor is a new state that occurs after an action is taken from a given state. For a given state, this must return three things: the successor state, the action required to get to the successor state, and the step cost. The last one is the incremental cost of expanding to that successor.

* get_cost_of_actions(): This returns the total cost of a particular sequence of actions. That sequence must be composed only of legal actions. 

In order to actually solve the problem, algorithms would have to be provided. Those algorithms go in the [search.py](https://github.com/jeffnyman/pacumen/blob/master/search.py) file, where placeholder methods exist for valid algorithms. The algorithms would use data structures -- provided in [structures.py](https://github.com/jeffnyman/pacumen/blob/master/library/structures.py) -- to carry out actions against a state and determine if the goal has been reached as a result of those actions.

This is about the bare minimum that you have to have in place to demonstrate a search algorithm. 

### Graphical Display

It will be necessary to eventually start drawing Pac-Man boards and the hardest part of graphics is ... well, the graphics. That's what the [graphical_support.py](https://github.com/jeffnyman/pacumen/blob/master/displays/graphical_support.py) module is attempting to provide. It's a very minimal sort of interface, using TKinter so as to reduce dependencies on alternative (and not built-in) graphics libraries.

This is minimal at best at this point. There is no provision at all for keybinding (meaning, interaction with the graphical display) and no provision at all for animation in the context of the display.
