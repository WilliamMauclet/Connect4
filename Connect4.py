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
	
	