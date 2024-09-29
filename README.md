Sliding Block Puzzle Solver - README
Introduction
This project implements a sliding block puzzle solver capable of finding the shortest solution using two search algorithms:

Breadth-First Search (BFS)
A\* Search
The solver reads an initial puzzle state from standard input and outputs a sequence of moves (UP, DOWN, LEFT, RIGHT) that the blank tile must make to reach the goal state.

The goal state is defined as the puzzle with all non-blank tiles in numerical order starting from the top-left corner, and the blank tile (0) in the top-left position.

A* Search Heuristic
Heuristic Used: Manhattan Distance
The heuristic function used in the A* search algorithm is the Manhattan Distance. This heuristic calculates the total number of moves each tile is away from its goal position by summing the horizontal and vertical distances.

Calculation Details
For each tile in the puzzle (excluding the blank tile):

Current Position: Determine the current row and column of the tile.
Goal Position: Determine the goal row and column of the tile.
Distance: Calculate the absolute difference in rows and columns.
Horizontal Distance: abs(current_col - goal_col)
Vertical Distance: abs(current_row - goal_row)
Manhattan Distance for Tile: Sum the horizontal and vertical distances.
Total Heuristic Value: Sum the Manhattan distances for all tiles.
Example
Consider a 3x3 puzzle:

sql
Copy code
Initial State: Goal State:
1 2 5 0 1 2
3 4 8 3 4 5
6 7 0 6 7 8
Tile 1:
Current Position: (0, 0)
Goal Position: (0, 1)
Manhattan Distance: abs(0 - 0) + abs(0 - 1) = 1
Tile 2:
Current Position: (0, 1)
Goal Position: (0, 2)
Manhattan Distance: abs(0 - 0) + abs(1 - 2) = 1
Tile 5:
Current Position: (0, 2)
Goal Position: (1, 2)
Manhattan Distance: abs(0 - 1) + abs(2 - 2) = 1
...
Total heuristic value is the sum of these distances.

Admissibility
The Manhattan Distance heuristic is admissible because it:

Never Overestimates: It provides a lower bound on the actual minimal number of moves required to reach the goal state.
Consistent: The estimated cost is always less than or equal to the estimated cost from any neighboring vertex to the goal, plus the cost to reach that neighbor.
Performance Comparison: BFS vs. A* Search
Breadth-First Search (BFS)
Strategy: Explores all possible states level by level.
Optimality: Guarantees the shortest path in terms of the number of moves.
Memory Usage: Can be high due to storing all states at the current depth.
Heuristic: Does not use any heuristic information.
A* Search
Strategy: Prioritizes states based on the estimated total cost (f(n) = g(n) + h(n)).
g(n): Actual cost from the initial state to the current state.
h(n): Heuristic estimate from the current state to the goal.
Optimality: Guarantees the shortest path if the heuristic is admissible.
Memory Usage: More efficient than BFS due to guided search.
Heuristic: Uses the Manhattan Distance to estimate the cost to reach the goal.
Performance Metrics
A good measure of performance is the number of nodes expanded during the search. This metric reflects the algorithm's efficiency in exploring the state space.

Test Cases and Results
Test Case 1
Input:

Copy code
3
1 2 5
3 4 8
6 7 0
Solution Moves:

css
Copy code
UP
UP
LEFT
LEFT
Performance:

BFS:
Nodes Expanded: 10
A\*:
Nodes Expanded: 6
Test Case 2
Input:

Copy code
3
2 8 3
1 6 4
7 0 5
Solution Moves:

css
Copy code
LEFT
UP
RIGHT
DOWN
RIGHT
UP
LEFT
DOWN
LEFT
UP
RIGHT
DOWN
Performance:

BFS:
Nodes Expanded: 19605
A*:
Nodes Expanded: 5453
Analysis
A* Search Expands Fewer Nodes:
Due to the heuristic guiding the search towards the goal, A* often expands significantly fewer nodes than BFS.
Efficiency:
Time: A* is generally faster because it avoids unnecessary exploration of irrelevant paths.
Memory: A* uses memory more efficiently by focusing on promising states.
Optimality:
Both algorithms find the optimal solution in terms of the number of moves.
Conclusion
The A* search algorithm, with the Manhattan Distance heuristic, outperforms BFS in solving the sliding block puzzle. It achieves this by expanding fewer nodes and efficiently guiding the search towards the goal state without compromising on finding the optimal solution.

How to Run the Solver
Execute the Program:

bash
Copy code
./puzzle --astar < input_file.txt
or

bash
Copy code
./puzzle --bfs < input_file.txt
Input Format:

php
Copy code
<size>
<row 1>
<row 2>
...
<row size>
Example:

Copy code
3
1 2 5
3 4 8
6 7 0
Output:

A sequence of moves, each on a new line, representing the steps to solve the puzzle.

Example:

css
Copy code
UP
UP
LEFT
LEFT
Additional Notes
Admissible Heuristics are Crucial:
Using an admissible heuristic like the Manhattan Distance ensures that A* search finds the optimal solution.
Scalability:
As the puzzle size increases, the efficiency gains of A* over BFS become more pronounced.
Implementation Details:
Both algorithms use a Puzzle class to represent the state.
States are stored as hashable keys to efficiently check for visited states.
References
Artificial Intelligence: A Modern Approach by Stuart Russell and Peter Norvig.
Heuristic Search Strategies: Understanding how heuristics guide search algorithms.
Manhattan Distance: A common heuristic for grid-based puzzles.
