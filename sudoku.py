import copy

def parse(text):
    return [[[] if c == "0" else [int(c)] for c in row] for row in text.split("\n")]

def emit(grid):
    return "\n".join(["".join([str(c[0] if len(c) > 0 else 0) for c in row]) for row in grid])

def get_row(grid, row_index):
    return grid[row_index]

def get_column(grid, column_index):
    return [row[column_index] for row in grid]

def get_subgrid(grid, subgrid_row_index, subgrid_column_index):
    subgrid = []
    for y in range(3*subgrid_row_index, 3*subgrid_row_index + 3):
        for x in range(3*subgrid_column_index, 3*subgrid_column_index + 3):
            subgrid.append(grid[y][x])
    return subgrid

def valid(shape):
    return all(len(c) != 1 or sum(c2.count(c[0]) for c2 in shape) == 1 for c in shape)

def complete(shape):
    return all(len(c) == 1 for c in shape)

def valid_row(grid, row_index):
    return valid(get_row(grid, row_index))

def valid_column(grid, column_index):
    return valid(get_column(grid, column_index))

def complete_row(grid, row_index):
    return complete(get_row(grid, row_index))

def complete_column(grid, column_index):
    return complete(get_column(grid, column_index))

def valid_subgrid(grid, subgrid_row_index, subgrid_column_index):
    return valid(get_subgrid(grid, subgrid_row_index, subgrid_column_index))

def complete_subgrid(grid, subgrid_row_index, subgrid_column_index):
    return complete(get_subgrid(grid, subgrid_row_index, subgrid_column_index))

def get_shapes(grid):
    for y in range(9):
        yield get_row(grid, y)
    for x in range(9):
        yield get_column(grid, x)
    for y in range(3):
        for x in range(3):
            yield get_subgrid(grid, y, x)
    raise StopIteration

def valid_grid(grid):
    return all(valid(s) for s in get_shapes(grid))

def complete_grid(grid):
    return all(complete(s) for s in get_shapes(grid))

def solved_grid(grid):
    return complete_grid(grid) and valid_grid(grid)

def add_possibilities(grid):
    for row in grid:
        for cell in row:
            if cell == []:
                cell.extend(range(1, 10))

def get_active_shapes(grid):
    for y in range(9):
        if grid[1][y]:
            yield [get_row(grid[0], y), y]
    for x in range(9):
        if grid[1][9 + x]:
            yield [get_column(grid[0], x), 9 + x]
    for y in range(3):
        for x in range(3):
            if grid[1][18 + y * 3 + x]:
                yield [get_subgrid(grid[0], y, x), 18 + y * 3 + x]
    raise StopIteration

def remove_taken_numbers(shape, grid):
    progress = False
    for cell in shape[0]:
        if len(cell) == 1:
            for cell_index in range(9):
                cell2 = shape[0][cell_index]
                if not cell is cell2 and cell[0] in cell2:
                    progress = True
                    cell2.remove(cell[0])
                    grid[2][shape[1]] = True
                    if shape[1] < 9:
                        # A row. So we also need to do the column and the subgrid.
                        grid[2][9 + cell_index] = True
                        grid[2][18 + (shape[1] / 3) * 3 + cell_index / 3] = True
                    elif shape[1] < 18:
                        # A col. Also do row and subgrid.
                        grid[2][cell_index] = True
                        grid[2][18 + (cell_index / 3) * 3 + (shape[1] - 9) / 3] = True
                    else:
                        # A subgrid. Also do row and col.
                        grid[2][((shape[1] - 18) / 3) * 3 + cell_index / 3] = True
                        grid[2][9 + ((shape[1] - 18) % 3) * 3 + cell_index % 3] = True
    return progress

def branches(grid):
    smallest_branches = 0
    smallest_branches_row_index = -1
    smallest_branches_cell_index = -1
    for row_index in range(len(grid[0])):
        row = grid[0][row_index]
        for cell_index in range(len(row)):
            cell = row[cell_index]
            if len(cell) > 1 and smallest_branches == 0 or len(cell) < smallest_branches:
                smallest_branches = len(cell)
                smallest_branches_row_index = row_index
                smallest_branches_cell_index = cell_index
                if smallest_branches == 2:
                    break
        if smallest_branches == 2:
            break
    if smallest_branches:
        for val in grid[0][smallest_branches_row_index][smallest_branches_cell_index]:
            branch = [copy.deepcopy(grid[0]), [False] * 27, [False] * 27]
            branch[0][smallest_branches_row_index][smallest_branches_cell_index] = [val]
            branch[2][smallest_branches_row_index] = True
            branch[2][9 + smallest_branches_cell_index] = True
            branch[2][18 + (smallest_branches_row_index / 3) * 3 + smallest_branches_cell_index / 3] = True
            yield branch
    raise StopIteration()

def unsolvable(grid):
    return any(any(c == [] for c in row) for row in grid)

def solve(grid):
    grid = copy.deepcopy(grid)
    add_possibilities(grid)
    grid = [grid, None, [True] * 27]
    def do_solve(grid):
        progress = True
        while progress:
            if unsolvable(grid[0]):
                return
            progress = False
            grid[1] = grid[2]
            grid[2] = [False] * 27
            for shape in get_active_shapes(grid):
                progress = remove_taken_numbers(shape, grid) or progress
        if solved_grid(grid[0]):
            return grid[0]
        for branch in branches(grid):
            b = do_solve(branch)
            if b:
                return b
        return None
    return do_solve(grid)