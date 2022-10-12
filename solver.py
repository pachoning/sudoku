import numpy as np
from initial import initial_board


def transform_indices(array):
    list_idx = []
    for x, y in zip(array[0], array[1]):
        list_idx.append([x, y])
    return np.array(list_idx)


def get_candidates(board):
    idx = np.where(board == -1)
    idx = transform_indices(idx)
    total_positions = idx.shape[0]
    found = False
    list_candidates = []
    i = 0
    while not found and i < total_positions:
        i += 1

    # If there are candidates, it must return:
    #   (found = True, [[row0, col0, number0], [row1, col1, number1], ...])
    # Otherwise:
    #   (found = False, [[-1, -1, -1]])
    return False, np.array([[]])


def recursive_sudoku(board, initial_indices):
    blank_idx = np.where(board == -1)
    total_blanck = len(blank_idx[0])

    # If the board is full, return it
    if total_blanck == 0:
        print("Finished")
        return board
    else:
        print("Not finished")
        # Look for all condidates
        found, candidates = get_candidates(board=board)
        print(found, candidates)

        # If no candidate, then delete one non-initial position at random
        # Return the board after deleting
        # If there are candidates, tale one randonmly and return the board


def solve_sudoku(board):
    idx = np.where(board == -1)
    initial_indices = transform_indices(array=idx)
    solution = recursive_sudoku(board=board, initial_indices=initial_indices)
    return solution


if __name__ == "__main__":
    solve_sudoku(board=initial_board)
