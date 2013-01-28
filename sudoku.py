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
    return all([len(c) != 1 or sum([c2.count(c[0]) for c2 in shape]) == 1 for c in shape])

def complete(shape):
    return all([len(c) == 1 for c in shape])

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
    shapes = []
    for y in range(9):
        shapes.append(get_row(grid, y))
    for x in range(9):
        shapes.append(get_column(grid, x))
    for y in range(3):
        for x in range(3):
            shapes.append(get_subgrid(grid, y, x))
    return shapes

def valid_grid(grid):
    return all([valid(s) for s in get_shapes(grid)])

def complete_grid(grid):
    return all([complete(s) for s in get_shapes(grid)])

def solved_grid(grid):
    return valid_grid(grid) and complete_grid(grid)

def add_possibilities(grid):
    for row in grid:
        for cell in row:
            if cell == []:
                cell.extend(range(1, 10))

def remove_taken_numbers(shape):
    progress = False
    for cell in shape:
        if len(cell) == 1:
            for cell2 in shape:
                if not cell is cell2 and cell[0] in cell2:
                    progress = True
                    cell2.remove(cell[0])
    return progress

def branches(grid):
    for row_index in range(len(grid)):
        row = grid[row_index]
        for cell_index in range(len(row)):
            cell = row[cell_index]
            if len(cell) > 1:
                for val in cell:
                    branch = copy.deepcopy(grid)
                    branch[row_index][cell_index] = [val]
                    yield branch
                raise StopIteration()
    raise StopIteration()

def solve(grid):
    grid = copy.deepcopy(grid)
    add_possibilities(grid)
    def do_solve(grid):
        progress = True
        while progress:
            progress = False
            for shape in get_shapes(grid):
                progress = remove_taken_numbers(shape) or progress
        if solved_grid(grid):
            return grid
        for branch in branches(grid):
            b = do_solve(branch)
            if b:
                return b
        return None
    return do_solve(grid)