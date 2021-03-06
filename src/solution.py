from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i]+cols[i] for i in range(len(rows))], 
                  [rows[i]+cols[-1-i] for i in range(len(rows))]]

unitlist = row_units + column_units + square_units + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_boxes = [k for k in values.keys() if len(values[k]) == 1]
    for box in solved_boxes:
        value = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(value, '')
            values = assign_value(values, peer, values[peer].replace(value, ''))
    return values

def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle
    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in "123456789":
            occurrences = [box for box in unit if digit in values[box]]
            if len(occurrences) == 1:
                #values[occurrences[0]] = digit
                values = assign_value(values, occurrences[0], digit)
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)
    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    result = values.copy()
    for unit in unitlist:
        # retrieve all unallocated boxes in this unit
        unsolved_boxes = [box for box in unit if len(values[box]) >= 2]
        if len(unsolved_boxes) >= 2:
            for i in range(len(unsolved_boxes)):
                for j in range(i + 1, len(unsolved_boxes)):
                    if values[unsolved_boxes[i]] == values[unsolved_boxes[j]] and len(values[unsolved_boxes[i]]) == 2 and len(values[unsolved_boxes[j]]) == 2:
                        # for each peer in this unit, remove the naked twins values
                        for k in [x for x in range(len(unsolved_boxes)) if x != i and x != j]:
                            for digit in values[unsolved_boxes[i]]:
                                result = assign_value(result, unsolved_boxes[k], result[unsolved_boxes[k]].replace(digit, ''))
    return result

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[box]) == 1 for box in boxes):
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    _, s = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_values = values.copy()
        #new_values[s] = value
        new_values = assign_value(new_values, s, value)
        result = search(new_values)
        if result:
            return result

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation
    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid) 
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print("We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.")
