import matplotlib.pyplot as plt
import numpy as np


def visualize_grid(grid, path=None):
    n, m = len(grid), len(grid[0])
    fig, ax = plt.subplots(figsize=(m, n))
    ax.set_xlim(-0.5, m - 0.5)
    ax.set_ylim(-0.5, n - 0.5)

    for i in range(n):
        for j in range(m):
            ax.text(
                j, n - i - 1, str(grid[i][j]), ha="center", va="center", fontsize=12
            )
            ax.add_patch(
                plt.Rectangle(
                    (j - 0.5, n - i - 1.5), 1, 1, fill=False, edgecolor="black"
                )
            )

    if path:
        x_coords, y_coords = zip(*[(j, n - i - 1) for i, j in path])
        ax.plot(x_coords, y_coords, color="red", linewidth=2, marker="o")

    plt.gca().set_aspect("equal", adjustable="box")
    plt.axis("off")
    plt.show()


def robot_coin_collection(board):
    """
    Computes the largest number of coins a robot can collect on an n x m board.

    Parameters:
    C (list of list of int): Matrix of size n x m where each cell contains either 1 (coin) or 0 (no coin).

    Returns:
    int: Largest number of coins the robot can collect to reach the bottom-right corner.
    """
    n = len(board)
    m = len(board[0])

    # Create a DP table with the same dimensions as the input matrix
    F = [[0] * m for _ in range(n)]

    # Initialize the starting position
    F[0][0] = board[0][0]

    # Fill the first row
    for j in range(1, m):
        F[0][j] = F[0][j - 1] + board[0][j]

    # Fill the rest of the DP table
    for i in range(1, n):
        F[i][0] = F[i - 1][0] + board[i][0]
        for j in range(1, m):
            F[i][j] = max(F[i - 1][j], F[i][j - 1]) + board[i][j]

    # Trace path
    path = trace_all_paths(F, board)

    # Return the result at the bottom-right corner
    return F, F[n - 1][m - 1], path


def trace_path(F, board):
    """
    Traces the path of the robot that collects the maximum number of coins (can find only 1 path).

    Parameters:
    F (list of list of int): DP table that stores the maximum number of coins collected at each cell.
    board (list of list of int): Original board.

    Returns:
    list of tuple: The path as a list of coordinates (i, j).
    """
    n = len(board)
    m = len(board[0])
    path = []

    # Start from the bottom-right corner
    i, j = n - 1, m - 1
    while i > 0 or j > 0:
        path.append((i, j))
        # Handle edge cases
        if i == 0:  # First row, can only move left
            j -= 1
        elif j == 0:  # First column, can only move up
            i -= 1
        else:  # General case: move from the larger value (up or left)
            if F[i - 1][j] > F[i][j - 1]:
                i -= 1  # Move up
            else:
                j -= 1  # Move left

    # Add the starting cell
    path.append((0, 0))
    path.reverse()  # Reverse the path to start from the beginning
    return path


def trace_all_paths(F, board, i=None, j=None, path=None):
    """
    Traces all possible paths for the robot to collect the maximum number of coins.

    Parameters:
    F (list of list of int): DP table.
    board (list of list of int): Original board.
    i, j (int, int): Current cell coordinates.
    path (list): Current path being traced.

    Returns:
    list of list of tuple: All possible paths.
    """
    if path is None:
        path = []
    if i is None or j is None:
        i, j = len(board) - 1, len(board[0]) - 1  # Start from the bottom-right corner

    path.append((i, j))

    if i == 0 and j == 0:  # Reached the starting cell
        return [path[::-1]]  # Reverse the path to start from (0, 0)

    paths = []
    if i > 0 and j > 0:  # General case
        if F[i - 1][j] > F[i][j - 1]:  # Move up
            paths.extend(trace_all_paths(F, board, i - 1, j, path[:]))
        elif F[i - 1][j] < F[i][j - 1]:  # Move left
            paths.extend(trace_all_paths(F, board, i, j - 1, path[:]))
        else:  # Both directions are valid
            paths.extend(trace_all_paths(F, board, i - 1, j, path[:]))
            paths.extend(trace_all_paths(F, board, i, j - 1, path[:]))
    elif i > 0:  # First column, can only move up
        paths.extend(trace_all_paths(F, board, i - 1, j, path[:]))
    elif j > 0:  # First row, can only move left
        paths.extend(trace_all_paths(F, board, i, j - 1, path[:]))

    return paths


# board = [
#     [0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0, 1],
#     [0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 1, 0],
# ]

# board = [
#     [0, 1, 0],
#     [1, 0, 0],
#     [1, 0, 1],
# ]

board = [
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1],
]


F, max_coint, paths = robot_coin_collection(board)
print("F", F)
visualize_grid(F)
print("Maximum coins collected:", max_coint)
for path in paths:
    print("Path to collect:", path)
    visualize_grid(F, path)
