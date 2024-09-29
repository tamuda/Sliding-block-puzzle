Usage: ./puzzle --astar < /u/cs242/hw2/test_in
You can change the algorithm to bfs

Heuristic Used: Manhattan Distance

In the A* search algorithm,  use the Manhattan Distance as the heuristic function. It calculates the sum of the horizontal and vertical distances of each tile from its goal position. For each tile (excluding the blank tile):

Current Position: The tile's row and column in the current state.
Goal Position: The tile's row and column in the goal state.
Manhattan Distance: abs(current_row - goal_row) + abs(current_col - goal_col)
The total heuristic value is the sum of the Manhattan distances for all tiles.

Here is why its admissible:

Never Overestimates: The Manhattan Distance provides the minimum number of moves required to reach the goal, so it does not overestimate the actual cost.
Ensures Optimality: Since the heuristic is admissible, the A* algorithm is guaranteed to find the shortest path to the goal state.


measured the performance of both algorithms by counting the number of nodes expanded during the search.

Test Input:

3
1 2 5
3 4 8
6 7 0
Results:
Breadth-First Search (BFS):
Nodes Expanded: 10
Solution Moves:

UP
UP
LEFT
LEFT
A* Search:
Nodes Expanded: 6
Solution Moves:

UP
UP
LEFT
LEFT


Efficiency: A* expanded fer nodes than BFS (6 vs 10), demonstrating higher efficiency.
Heuristic Guidance: The Manhattan Distance heuristic in A* effectively guides the search towards the goal, reducing unnecessary explorations.
Optimality: Both algorithms found the optimal solution with the shortest number of moves.