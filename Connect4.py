# Een
class RowOfRowsGrid:
	def clear():
		self.grid = [ [] for i in range(0,6)]
	def getRow(index):
		return self.grid[index]
	def isRowNotFull(index):
		return len(self.grid[index])) <= 7
	def getAvailableRows():
		return [ index for index in range(0,6) if isRowNotFull(index)]
	def dropPiece(row, player):
		self.grid[row].append(player)
	def checkConsistency():
		for row in grid:
			assert(len(row) <= 7)
	def gameOver():
		raise NotImplementedError('hmmm')
		
# Twee
# Volgens mij is die Point klasse en dict niet nodig, kan ik enkel rijen, kolommen en diagonalen bewaren

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
class DictOfPointsGrid:
	def clear():
		self.rows = [ [] for i in range(0,7)] 
		self.columns = [ [] for i in range(0,6)] 
		#2*(2*1+2*2+2*3)
		self.significantDiagonals = [ [] for i in range(0,24)]
		
		for i in range(0,6):
			for j in range(0,7):
				self.grid[Point(i,j), None]
				self.rows
		
	def addPoint(point):
		
	def getRow(index):
		
# Three

class DictOfPointsGrid:
	def clear():
		self.rows = [ [ None for i in range(0,6) ] for i in range(0,7)] 
		self.columns = [ [ None for i in range(0,6)] for i in range(0,7)] 
		#2*(2*1+2*2+2*3)
		self.diagonals = [ [ None for j in range(1,i%6)] for i in range(0,24)]
			
		for i in range(0,6):
			for j in range(0,7):
				self), None]
				self.rows
		
	def addPoint(point):
		
	def getRow(index):
		
# x  x  x  x  x  x  x
# x  x  x  x  x  x  x
# x  x  x  x  x  x  x 
# 0  2  5  8  x  x  x 
# 1  4  7  10 x  x  x 
# 3  6  9  x  x  x  x 

# 0: (0,3),(1,4),(2,5),(3,6)
# 1: (0,2),(1,3),(2,4),(4,5)
# 2: (1,3),(2,4),(3,5),(4,6)
# 3: (0,0),(1,1),(2,2)(3,3),(4,4)
# 4: (1,1),(2,2)(3,3),(4,4),(5,5)
# 5: (2,2)(3,3),(4,4),(5,5),(6,6)
# 6: (1,0),(2,0),(3,0),(4,0)

# => Better: just look at diagonals of length >=4
		
# only keep columns
class ColumnGrid:
	def clear(self):
		self.columns = [ [ None for i in range(0,6)] for i in range(0,7)] 
		PLAYER_ID_1 = 'X'
		PLAYER_ID_2 = 'O'
	def getColumn(self, x):
		return self.columns[x]
	def addPawn(self, x, playerId):
		for y in range(0,6):
			if self.columns(column, y) is None:
				self.columns(column, y) = playerId
				return
		assert False, "Column " + str(column) + " was already full." + getGrid
	def checkConsistency(self):
		assert len(self.columns) is 7, str(len(self.columbs) + " many columns found O.o"
		nrPawnsDict = {None:0,PLAYER_ID_1:0,PLAYER_ID_2:0}
		for column in self.columns:
			assert len(column) is 6, "Column " + str(column) + " has " + len(column) + " tiles! " + str(column) 
			for tile in column:
				nrPawnsDict[tile] += nrPawnsDict[tile]
		assert nrPawnsDict 
	def fourInARow(row):
		seq = 0
		prev = None
		for tile in row:
			if tile is None:
				seq = 0
			elif tile is prev:
				seq += 0
				
			if seq = 4:
				return tile
			prev = tile
		return False
	
	def getLeftUpDiagonal(self, x, y):
		row = []
		while x < 7 and y < 6:
			row.append(self.columns[x][y])
			x += 1
			y += 1
		return row
	
		
	def gameOver(self):
		for column in self.columns:
			if not fourInARow(column):
				return fourInARow(colummn)
		for y in range(0,6):
			row = [self.columns[x, y] for x in range(0,7)]
			if not fourInARow(row):
				return fourInARow(row)
		
		for x in range(0,6):
			diagonal = [self.columns]
			
		raise NotImplementedError('Not implemented yet :/')
	
	