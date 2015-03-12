import time
class lifeGrid:
	def __init__(self,coordList):
		self.coordList = coordList
		self.minRow = min(i[0] for i in coordList)
		self.minCol = min(i[1] for i in coordList)
		self.maxRow = max(i[0] for i in coordList)
		self.maxCol = max(i[1] for i in coordList)
	def minRange(self):
		return (self.minRow,self.minCol)
	def maxRange(self):
		return (self.maxRow,self.maxCol)
	def setCell(self,row,col):
		if row > self.maxRow:
			self.maxRow = row
		elif row < self.minRow:
			self.minRow = row
		if col > self.maxCol:
			self.maxCol = col
		elif col < self.minCol:
			self.minCol = col
		theCell = (row,col)
		self.coordList.append(theCell)
	def isAlive (self,row,col):
		theCell = (row,col)
		return theCell in self.coordList
	def numAliveNeighbors(self,row,col):
		count = 0
		for theRow in range(row-1,row+2):
			for theCol in range(col-1,col+2):
				if theRow == row and theCol == col:
					continue
				if self.isAlive(theRow,theCol):
					count += 1
		return count
	def draw(self):
		for theRow in range(self.minRow-2,self.maxRow + 3):
			rowStr = ''
			for theCol in range(self.minCol-2,self.maxCol + 3):
				theCell = (theRow,theCol)
				if theCell in self.coordList:
					rowStr += '@'
				else:
					rowStr += '.'
			print rowStr
		print
	def evolve(self):
		newList = list()
		for theRow in range(self.minRow-1,self.maxRow + 2):
			for theCol in range(self.minCol-1,self.maxCol + 2):
				neighbors = self.numAliveNeighbors(theRow,theCol)
				if (neighbors == 2 and self.isAlive(theRow,theCol)) or (neighbors == 3):
					newList.append((theRow,theCol))
		self.coordList = newList
		self.minRow = min(i[0] for i in newList)
		self.minCol = min(i[1] for i in newList)
		self.maxRow = max(i[0] for i in newList)
		self.maxCol = max(i[1] for i in newList)
def main():
	coordList = [(0,0),(1,1),(1,2),(0,2),(-1,2)]
	grid = lifeGrid(coordList)
	for i in range(20):
		grid.draw()
		grid.evolve()
		time.sleep(0.5)

main() 