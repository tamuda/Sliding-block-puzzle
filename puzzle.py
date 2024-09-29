#!/usr/bin/env python3

import sys
from copy import deepcopy
from typing import List, Tuple, Optional

class Puzzle:
    """
    Class representing the sliding puzzle board.
    """

    def __init__(self, board: List[List[int]], size: int):
        """
        Initializes the Puzzle instance.

        :param board: 2D list representing the puzzle board.
        :param size: Size of the puzzle (e.g., 3 for a 3x3 puzzle).
        """
        self.board = board
        self.size = size
        self.blank_pos = self._find_blank()

    def _find_blank(self) -> Tuple[int, int]:
        """
        Finds the position of the blank tile (0) in the puzzle.

        :return: Tuple (row, column) of the blank tile.
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return (row, col)
        raise ValueError("Blank tile (0) not found in the puzzle.")

    def get_possible_moves(self) -> List[str]:
        """
        Determines the valid moves (UP, DOWN, LEFT, RIGHT) from the current blank position.

        :return: List of valid moves as strings.
        """
        moves = []
        row, col = self.blank_pos

        if row > 0:
            moves.append('UP')
        if row < self.size - 1:
            moves.append('DOWN')
        if col > 0:
            moves.append('LEFT')
        if col < self.size - 1:
            moves.append('RIGHT')

        return moves

    def move_blank(self, direction: str) -> 'Puzzle':
        """
        Moves the blank tile in the specified direction and returns a new Puzzle instance.

        :param direction: Direction to move ('UP', 'DOWN', 'LEFT', 'RIGHT').
        :return: New Puzzle instance with the move applied.
        """
        row, col = self.blank_pos
        new_board = deepcopy(self.board)

        if direction == 'UP':
            target_row, target_col = row - 1, col
        elif direction == 'DOWN':
            target_row, target_col = row + 1, col
        elif direction == 'LEFT':
            target_row, target_col = row, col - 1
        elif direction == 'RIGHT':
            target_row, target_col = row, col + 1
        else:
            raise ValueError(f"Invalid move direction: {direction}")

        # Swap the blank with the target tile
        new_board[row][col], new_board[target_row][target_col] = (
            new_board[target_row][target_col],
            new_board[row][col],
        )

        return Puzzle(new_board, self.size)

    def is_goal_state(self, goal_board: List[List[int]]) -> bool:
        """
        Checks if the current puzzle state matches the goal state.

        :param goal_board: 2D list representing the goal puzzle board.
        :return: True if current state is the goal state, False otherwise.
        """
        return self.board == goal_board

    def get_state_key(self) -> Tuple[Tuple[int, ...], ...]:
        """
        Generates a hashable and unique key for the current state.

        :return: Tuple of tuples representing the puzzle board.
        """
        return tuple(tuple(row) for row in self.board)

    def __eq__(self, other: 'Puzzle') -> bool:
        return self.board == other.board

    def __hash__(self):
        return hash(self.get_state_key())

    def __str__(self):
        """
        Returns a string representation of the puzzle board.

        :return: String representation.
        """
        return '\n'.join(' '.join(map(str, row)) for row in self.board)


def parse_input(input_lines: List[str]) -> Puzzle:
    """
    Parses the input lines to create the initial Puzzle instance.

    :param input_lines: List of input lines as strings.
    :return: Puzzle instance representing the initial state.
    """
    size = int(input_lines[0])
    board = [list(map(int, line.strip().split())) for line in input_lines[1:size + 1]]
    return Puzzle(board, size)


def generate_goal_state(size: int) -> List[List[int]]:
    """
    Generates the goal state for a puzzle of the given size.

    :param size: Size of the puzzle.
    :return: 2D list representing the goal puzzle board.
    """
    goal = [list(range(i * size, (i + 1) * size)) for i in range(size)]
    # Place the blank tile (0) at the top-left corner
    goal[0][0] = 0
    count = 1
    for i in range(size):
        for j in range(size):
            if i == 0 and j == 0:
                continue
            goal[i][j] = count
            count += 1
    return goal


def main():
    # Read input from stdin
    input_lines = sys.stdin.read().strip().split('\n')
    puzzle = parse_input(input_lines)
    goal_board = generate_goal_state(puzzle.size)

    # For demonstration purposes, print the initial and goal states
    print("Initial State:")
    print(puzzle)
    print("\nGoal State:")
    print('\n'.join(' '.join(map(str, row)) for row in goal_board))

def heuristic(puzzle: Puzzle, goal_positions: Dict[int, Tuple[int, int]]) -> int:
    """
    Calculates the heuristic value (Manhattan Distance) for the puzzle.

    :param puzzle: The current Puzzle instance.
    :param goal_positions: Dictionary mapping tile numbers to their goal positions.
    :return: Heuristic value as an integer.
    """
    distance = 0
    for row in range(puzzle.size):
        for col in range(puzzle.size):
            tile = puzzle.board[row][col]
            if tile != 0:
                goal_row, goal_col = goal_positions[tile]
                distance += abs(row - goal_row) + abs(col - goal_col)
    return distance


def astar_search(initial_puzzle: Puzzle, goal_board: List[List[int]]) -> Optional[List[str]]:
    """
    Performs the A* search algorithm to find the shortest path to the goal state.

    :param initial_puzzle: The initial Puzzle instance.
    :param goal_board: 2D list representing the goal puzzle board.
    :return: List of moves leading to the solution, or None if no solution exists.
    """
    goal_positions = {}
    for i in range(len(goal_board)):
        for j in range(len(goal_board)):
            goal_positions[goal_board[i][j]] = (i, j)

    open_set = []
    heapq.heappush(open_set, (0, initial_puzzle))
    came_from = {}
    g_score = {initial_puzzle.get_state_key(): 0}
    f_score = {initial_puzzle.get_state_key(): heuristic(initial_puzzle, goal_positions)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current.is_goal_state(goal_board):
            return reconstruct_path(came_from, current)

        for move in current.get_possible_moves():
            neighbor = current.move_blank(move)
            tentative_g_score = g_score[current.get_state_key()] + 1
            neighbor_key = neighbor.get_state_key()

            if neighbor_key not in g_score or tentative_g_score < g_score[neighbor_key]:
                came_from[neighbor_key] = (current, move)
                g_score[neighbor_key] = tentative_g_score
                f_score_neighbor = tentative_g_score + heuristic(neighbor, goal_positions)
                f_score[neighbor_key] = f_score_neighbor
                heapq.heappush(open_set, (f_score_neighbor, neighbor))

    return None  # No solution found


def reconstruct_path(came_from: Dict[Tuple[Tuple[int, ...], ...], Tuple[Puzzle, str]], current: Puzzle) -> List[str]:
    """
    Reconstructs the path from the initial state to the goal state.

    :param came_from: Dictionary mapping state keys to their predecessors and moves.
    :param current: The current Puzzle instance (goal state).
    :return: List of moves leading to the solution.
    """
    total_path = []
    current_key = current.get_state_key()
    while current_key in came_from:
        current, move = came_from[current_key]
        total_path.append(move)
        current_key = current.get_state_key()
    return total_path[::-1]  # Reverse the path to get the correct order

if __name__ == "__main__":
    main()
