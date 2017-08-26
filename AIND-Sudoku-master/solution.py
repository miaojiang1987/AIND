assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy only on the columns.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    all_digits = '123456789'
    
    for unit in row_units + column_units + square_units:
        d = dict()
        for digit in all_digits:
            # get all boxes in the unit that have the digit
            boxes_with_digit = ''.join([box for box in unit if digit in values[box]])
            # if a digit is only in 2 boxes:
            if len(boxes_with_digit) == 4:
                # Insert the concatenated boxes names as the key in a dictionary with digit as the value 
                if (boxes_with_digit not in d.keys()): 
                    # print('inserting:', digit, ' in ', boxes_with_digit)
                    d[boxes_with_digit] = digit
                # If the concatenated boxes names are already in the dictionary, we have a twin!
                else:
                    digits = d[boxes_with_digit] + digit
                    # print('updating:', digits, ' in ', boxes_with_digit)

                    for box in unit:
                        if (box in boxes_with_digit):
                            # These 2 boxes must have only these 2 values
                            assign_value(values, box, digits) #values[box] = digits
                            
                        else:
                            # The rest of the boxes cannot have these digits
                            assign_value(values, box, values[box].replace(digits[0], ""))
                            assign_value(values, box, values[box].replace(digits[1], ""))
                            # values[box] = values[box].replace(digits[0], "")
                            # values[box] = values[box].replace(digits[1], "")
    return values
 
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r+c for r in A for c in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ('ABC','DEF','GHI') for c in ('123','456','789')]
diag1 = [[str(r)+str(10- int(c)) for (r,c) in zip(rows,cols)]]
diag2 = [[r+c for (r,c) in zip(rows,cols)]]
unitlist = row_units + column_units + square_units + diag1 + diag2

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    chars = []
    digits = '123456789'
    for c in grid:
        if c == '.':
            chars.append(digits)
        if c in digits:
            chars.append(c)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

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
    
def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,'')) 
            # values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    all_digits = '123456789'

    for unit in unitlist:
        for digit in all_digits:
            # get all boxes in the unit that have the digit
            boxes_with_digit = [box for box in unit if digit in values[box]]
            # if there is only 1 box, update it
            if len(boxes_with_digit) == 1:
                assign_value(values, boxes_with_digit[0], digit) 
                # values[boxes_with_digit[0]] = digit
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked twins strategy
        values = naked_twins(values) 
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    values = grid_values(grid)
    return search(values)

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Chose one of the unfilled square s with the fewest possibilities
    unsolved_values = [box for box in values.keys() if len(values[box]) > 1]
    # print(len(unsolved_values))
    if len(unsolved_values) > 0:
        box, vals = sorted(values.items(), key = lambda x: 10 if (len(x[1]) <= 1) else len(x[1]))[0]
        # print(box, vals)
        for v in vals:
            values_try = values.copy()
            assign_value(values_try, box, v) 
            # values_try[box] = v
            solve_try = search(values_try)
            if solve_try:
                return solve_try
    else:
        return values
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve((diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
