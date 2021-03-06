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

### Layouts

The graphical display mentioned above has to come from somewhere. Ideally these Pac-Man boards should be easy to create. And "easy to create" and "graphical design" do not always go hand-in-hand. So Pacumen is based on the concept of textual layouts serving as the basis for the graphical layouts.

The idea is that a maze will be encoded as a layout (see [test_maze.lay](https://github.com/jeffnyman/pacumen/blob/master/layouts/test_maze.lay)). This becomes part of an internal layout representation, implemented in [layout.py](https://github.com/jeffnyman/pacumen/blob/master/mechanics/layout.py), which is in turn a type of grid, implemented in [grid.py](https://github.com/jeffnyman/pacumen/blob/master/mechanics/grid.py).  

Consider this layout:

    %%%%%%%
    %    P%
    % %%% %
    %  %  %
    %%   %%
    %. %%%%
    %%%%%%%

Here the % symbols represent the walls of the maze. Any periods represent food dots. The letter P indicates the Pac-Man agent.

Here is the (x,y) representation that Paucmen generates for the above layout:

    0,6  1,6  2,6  3,6  4,6  5,6  6,6
     %    %    %    %    %    %    %
    0,5  1,5  2,5  3,5  4,5  5,5  6,5
     %                        P    %
    0,4  1,4  2,4  3,4  4,4  5,4  6,4
     %         %    %    %         %
    0,3  1,3  2,3  3,3  4,3  5,3  6,3
     %              %              %
    0,2  1,2  2,2  3,2  4,2  5,2  6,2
     %    %                   %    %
    0,1  1,1  2,1  3,1  4,1  5,1  6,1
     %    .         %    %    %    %
    0,0  1,0  2,0  3,0  4,0  5,0  6,0
     %    %    %    %    %    %    %

Note that the grid treats the lower left corner as the origin, just as in mathematics:

![grid-lower-left](http://testerstories.com/files/pacumen/grid-lower-left.png)

Specifically, the origin in a graph of positive numbers is in the lower-left. In gaming terms, the origin is usually taken to be the top left, due to how pixels are rendered on the screen. However, the basis of Pacumen is ultimately a mathematical representation, which is why it follows that standard.

What this means is that the above should represent as such in a graphical context:

![pacumen-grid](http://testerstories.com/files/pacumen/pacumen-grid.png)

While the above (x,y) representation works, Pacumen actually uses a (y,x) representation, as such:

    6,0  6,1  6,2  6,3  6,4  6,5  6,6
     %    %    %    %    %    %    %
    5,0  5,1  5,2  5,3  5,4  5,5  5,6
     %                        P    %
    4,0  4,1  4,2  4,3  4,4  4,5  4,6
     %         %    %    %         %
    3,0  3,1  3,2  3,3  3,4  3,5  3,6
     %              %              %
    2,0  2,1  2,2  2,3  2,4  2,5  2,6
     %    %                   %    %
    1,0  1,1  1,2  1,3  1,4  1,5  1,6
     %    .         %    %    %    %
    0,0  0,1  0,2  0,3  0,4  0,5  0,6
     %    %    %    %    %    %    %

Looking at the two grids, I just like how the (y,x) version reads more than the (x,y). Programmatically, as the layout is constructed into a grid, the walls are represented like this:

    TTTTTTT
    TFFFFFT
    TFTTTFT
    TFFTFFT
    TTFFFTT
    TFFTTTT
    TTTTTTT

Here every T is a wall.

The dot locations are represented like this:

    FFFFFFF
    FFFFFFF
    FFFFFFF
    FFFFFFF
    FFFFFFF
    FTFFFFF
    FFFFFFF

Here the dot location -- and there's only one -- is shown as a T (second row up from the bottom).

It's important to note that because the layout is read from the bottom to the top, when the walls or food grid representations are printed, they must be done in reverse.
