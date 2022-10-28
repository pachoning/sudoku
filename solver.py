import time
import numpy as np
from initial import initial_board
import sys


sys.setrecursionlimit(1000000)


def transform_indices(array):
    list_idx = []
    for x, y in zip(array[0], array[1]):
        list_idx.append([x, y])
    return np.array(list_idx)


def get_numbers_square(board, row_idx, column_idx):
    q_row = row_idx // 3
    q_column = column_idx // 3
    row_ini = 3 * q_row
    row_end = row_ini + 2 + 1
    column_ini = 3 * q_column
    column_end = column_ini + 2 + 1
    numbers = board[row_ini:row_end, column_ini:column_end]
    numbers = np.reshape(numbers, newshape=(1, -1))
    return numbers


def get_all_candidates(board, impossible_boards):
    # Get all the positions without a number
    #print("\timpossible_boards")
    #print(impossible_boards)
    idx = transform_indices(array=np.where(board == -1))
    possible_options = np.arange(1, 10)
    total_empty_cells = idx.shape[0]
    list_information = []
    i = 0
    while i < total_empty_cells:
        cell_information = []
        # Get the empty cell
        empty_cell_idx = idx[i]
        row_idx = empty_cell_idx[0]
        column_idx = empty_cell_idx[1]
        # Get all numbers in the row
        all_numbers_row = np.reshape(board[row_idx, :], newshape=(1, -1))
        # Get all numbers in the column
        all_numbers_column = np.reshape(board[:, column_idx], newshape=(1, -1))
        # Get all numbers in the square
        all_numbers_square = get_numbers_square(board=board, row_idx=row_idx, column_idx=column_idx)
        # Join them (J)
        all_numbers = np.concatenate((all_numbers_row, all_numbers_column, all_numbers_square), axis=1)
        all_numbers = np.unique(all_numbers)
        # Get the difference between {1, 2, ..., 9} and J
        diff = []
        for x in possible_options:
            if not x in all_numbers:
                temp_board = np.copy(board)
                temp_board[row_idx, column_idx] = x
                #print("\tTemp board:\n", temp_board)
                impossible = check_impossible(board=temp_board, impossible_boards=impossible_boards)
                #print("\timpossible:", impossible)
                if not impossible:
                    diff.append(x)        
        total_candidates = len(diff)

        if total_candidates > 0:
            cell_information.append(row_idx)
            cell_information.append(column_idx)
            cell_information.append(total_candidates)
            cell_information.append(diff)
            list_information.append(cell_information)
        i += 1
    return list_information


def choose_candidate_to_delete(axis_element, by_row, initial_indices, empty_indices):
    valid_candidate = False
    while not valid_candidate:
        random_element = np.random.choice(a=9, size=1)
        if by_row:
            idx = [axis_element, random_element]
        else:
            idx = [random_element, axis_element]
        is_initial_index = idx in initial_indices.tolist()
        already_empty = idx in empty_indices.tolist()
        valid_candidate = (not is_initial_index) and (not already_empty)
    return idx


def get_position_to_delete(initial_candidates):
    # Delete an element which has the highest number of inital candidates 
    number_candidates = [x[2] for x in initial_candidates]
    max_num_initial_candidates = np.max(number_candidates)
    idx_candidates = [i for i, x in enumerate(initial_candidates) if x[2] == max_num_initial_candidates]
    idx_selected_candidate = np.random.choice(a=idx_candidates, size=1)
    idx_selected_candidate = idx_selected_candidate[0]
    element_to_delete = initial_candidates[idx_selected_candidate]
    list_positions = [element_to_delete[0], element_to_delete[1]]
    return list_positions


def select_candidate(candidates):
    if len(candidates) == 0:
        found = False
        selected_candidated = [-1, -1, -1]
    else:
        found = True
        num_candidates = [x[2] for x in candidates]
        min_num_candidates = min(num_candidates)
        list_candidates = [i for i, x in enumerate(candidates) if x[2] == min_num_candidates]
        idx_candidate = np.random.choice(a=list_candidates, size=1)
        idx_candidate = idx_candidate[0]
        selected_candidate = candidates[idx_candidate]
        number = np.random.choice(a=selected_candidate[3], size=1)
        number = number[0]
        selected_candidated = [selected_candidate[0], selected_candidate[1], number]
    return found, selected_candidated


def check_impossible(board, impossible_boards):
    impossible = False
    num_impossible_boards = len(impossible_boards)
    if num_impossible_boards > 0:
        i = 0
        #print("inside check_impossible")
        #print("board")
        #print(board)
        while i < num_impossible_boards and not impossible:
            impossible_board_i = impossible_boards[i]
            #print("impossible_board_i")
            #print(impossible_board_i)
            comparison = impossible_board_i == board
            impossible = comparison.all()
            #print("comparison:", comparison)
            i += 1
        #print("impossible:", impossible)
    return impossible

def recursive_sudoku(board, initial_indices, initial_candidates, impossible_boards):
    empty_idx = np.where(board == -1)
    total_empty = len(empty_idx[0])
    print("total_empty:", total_empty)
    print(board)
    # If the board is full, return it
    if total_empty == 0:
        #print("Finished")
        return board
    else:
        #print("Not finished")
        # Get all the candidates
        #print("-------------------------")
        #print("Current board")
        #print(board)
        all_candidates = get_all_candidates(board=board, impossible_boards=impossible_boards)
        # Select the position with the smallest number of candidares
        found, candidate = select_candidate(all_candidates)
        #print("\tcandidate found:", found)
        #print("\tcandidate:", candidate)
        if found:
            #print("Candidate found")
            #print("candidate to insert:", candidate)
            row_idx = candidate[0]
            column_idx = candidate[1]
            number = candidate[2]
            board[row_idx, column_idx] = number
            #print(board)
         # If no candidate, then delete non-initial positions
        else:
            impossible_boards.append(np.copy(board))
            #print("\timpossible_boards")
            #print(impossible_boards)
            # Delete the position with the greatest number of initial candidates
            postion_to_delete = get_position_to_delete(initial_candidates=initial_candidates)
            #print("\tPositions to delete:", postion_to_delete)
            #print(board)
            board[postion_to_delete[0], postion_to_delete[1]] = -1
            #time.sleep(1)
        return recursive_sudoku(board=board, initial_indices=initial_indices, initial_candidates=initial_candidates, impossible_boards=impossible_boards)


def solve_sudoku(board):
    idx = np.where(board > -1)
    initial_indices = transform_indices(array=idx)
    impossible_boards = []
    initial_candidates = get_all_candidates(board=board, impossible_boards=impossible_boards)
    solution = recursive_sudoku(
        board=board,
        initial_indices=initial_indices,
        initial_candidates=initial_candidates,
        impossible_boards=impossible_boards,
    )
    return solution


if __name__ == "__main__":
    solve_sudoku(board=initial_board)
