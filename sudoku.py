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

def solve(grid):
    return grid