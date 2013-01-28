import sudoku
import unittest

class Tests(unittest.TestCase):

	def setUp(self):
		self.sudokuText = """407900630
030800009
000563000
504700020
029030460
070002801
000354000
700009080
065008304"""
		self.sudokuGrid = [[[4],[],[7],[9],[],[],[6],[3],[]],[[],[3],[],[8],[],[],[],[],[9]],[[],[],[],[5],[6],[3],[],[],[]],[[5],[],[4],[7],[],[],[],[2],[]],[[],[2],[9],[],[3],[],[4],[6],[]],[[],[7],[],[],[],[2],[8],[],[1]],[[],[],[],[3],[5],[4],[],[],[]],[[7],[],[],[],[],[9],[],[8],[]],[[],[6],[5],[],[],[8],[3],[],[4]]]
		self.sudokuGridSolved = [[[4],[5],[7],[9],[2],[1],[6],[3],[8]],[[6],[3],[2],[8],[4],[7],[5],[1],[9]],[[9],[8],[1],[5],[6],[3],[7],[4],[2]],[[5],[1],[4],[7],[8],[6],[9],[2],[3]],[[8],[2],[9],[1],[3],[5],[4],[6],[7]],[[3],[7],[6],[4],[9],[2],[8],[5],[1]],[[2],[9],[8],[3],[5],[4],[1],[7],[6]],[[7],[4],[3],[6],[1],[9],[2],[8],[5]],[[1],[6],[5],[2],[7],[8],[3],[9],[4]]]

	def test_parse(self):
		self.assertEqual(sudoku.parse(self.sudokuText), self.sudokuGrid)

	def test_emit(self):
		self.assertEqual(sudoku.emit(self.sudokuGrid), self.sudokuText)

	def test_valid_row(self):
		self.assertTrue(sudoku.valid_row(self.sudokuGrid, 3))
		self.sudokuGrid[0][0] = [3]
		self.assertFalse(sudoku.valid_row(self.sudokuGrid, 0))

	def test_valid_column(self):
		self.assertTrue(sudoku.valid_column(self.sudokuGrid, 3))
		self.sudokuGrid[0][0] = [5]
		self.assertFalse(sudoku.valid_column(self.sudokuGrid, 0))

	def test_complete_row(self):
		self.assertFalse(sudoku.complete_row(self.sudokuGrid, 3))
		self.sudokuGrid[0] = [[9], [2], [3], [4], [5], [6], [7], [8], [1]]
		self.assertTrue(sudoku.complete_row(self.sudokuGrid, 0))

	def test_complete_column(self):
		self.assertFalse(sudoku.complete_column(self.sudokuGrid, 3))
		for x in range(9):
			self.sudokuGrid[x][0] = [9 - x]
		self.assertTrue(sudoku.complete_column(self.sudokuGrid, 0))

	def test_valid_subgrid(self):
		self.assertTrue(sudoku.valid_subgrid(self.sudokuGrid, 1, 2))
		self.sudokuGrid[4][7] = [4]
		self.assertFalse(sudoku.valid_subgrid(self.sudokuGrid, 1, 2))

	def test_complete_subgrid(self):
		self.assertFalse(sudoku.complete_subgrid(self.sudokuGrid, 0, 1))
		self.sudokuGrid[0] = [[4],[ ],[7],[9],[1],[2],[6],[3],[ ]]
		self.sudokuGrid[1] = [[ ],[3],[ ],[8],[4],[7],[ ],[ ],[9]]
		self.sudokuGrid[2] = [[ ],[ ],[ ],[5],[6],[3],[ ],[ ],[ ]]
		self.assertTrue(sudoku.complete_subgrid(self.sudokuGrid, 0, 1))

	def test_valid_grid(self):
		self.assertTrue(sudoku.valid_grid(self.sudokuGrid))
		self.sudokuGrid[0][0] = [5]
		self.assertFalse(sudoku.valid_grid(self.sudokuGrid))
		self.sudokuGrid[8][8] = [5]
		self.assertFalse(sudoku.valid_grid(self.sudokuGrid))
		self.sudokuGrid[0][4] = [8]
		self.assertFalse(sudoku.valid_grid(self.sudokuGrid))

	def test_complete_grid(self):
		self.assertFalse(sudoku.complete_grid(self.sudokuGrid))
		self.assertTrue(sudoku.complete_grid(self.sudokuGridSolved))
		
	def test_solve(self):
	    self.assertEqual(sudoku.solve(self.sudokuGrid), self.sudokuGridSolved)

if __name__ == '__main__':
	unittest.main()
