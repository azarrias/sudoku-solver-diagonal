from collections import defaultdict

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]

boxes = cross(rows, cols)
history = {}  # history must be declared here so that it exists in the assign_values scope

def extract_units(unitlist, boxes):
    """Initialize a mapping from box names to the units that the boxes belong to
    Parameters
    ----------
    unitlist(list)
        a list containing "units" (rows, columns, diagonals, etc.) of boxes
    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)
    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    """
    # the value for keys that aren't in the dictionary are initialized as an empty list
    units = defaultdict(list)
    for current_box in boxes:
        for unit in unitlist:
            if current_box in unit:
                # defaultdict avoids this raising a KeyError when new keys are added
                units[current_box].append(unit)
    return units

def extract_peers(units, boxes):
    """Initialize a mapping from box names to a list of peer boxes (i.e., a flat list
    of boxes that are in a unit together with the key box)
    Parameters
    ----------
    units(dict)
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)
    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a set
        containing all boxes that are peers of the key box (boxes that are in a unit
        together with the key box)
    """
    # the value for keys that aren't in the dictionary are initialized as an empty list
    peers = defaultdict(set)  # set avoids duplicates
    for key_box in boxes:
        for unit in units[key_box]:
            for peer_box in unit:
                if peer_box != key_box:
                    # defaultdict avoids this raising a KeyError when new keys are added
                    peers[key_box].add(peer_box)
    return peers

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
