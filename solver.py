import numpy as np
from initial import initial_board


def transform_indices(array):
    list_idx = []
    for x, y in zip(array[0], array[1]):
        list_idx.append([x, y])
    return np.array(list_idx)


def get_candidate(board):
    # Get all the positions without a number
    idx = transform_indices(array=np.where(board == -1))
    total_empty_cells = idx.shape[0]
    found = False
    i = 0
    while not found and i < total_empty_cells:
        # Get the empty cell
        # Get all numbers in the row
        # Get all numbers in the column
        # Get all numbers in the square
        # Join them (J)
        # Get the difference between {1, 2, ..., 9} and J
        # If there is a candiate, stop and store it
        # Otherwise, keep loopong
        i += 1

    # If there is a candidate, return:
    #   (found = True, [[row, col, number])
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
        found, candidate = get_candidate(board=board)
        print(found, candidate)

        # If no candidate, then delete one non-initial position at random
        # Return the board after deleting
        # If there is a candidate, tale one randonmly and return the board


def solve_sudoku(board):
    idx = np.where(board == -1)
    initial_indices = transform_indices(array=idx)
    solution = recursive_sudoku(board=board, initial_indices=initial_indices)
    return solution


if __name__ == "__main__":
    solve_sudoku(board=initial_board)
