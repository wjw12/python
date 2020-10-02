import ctypes
class array:
	def __init__(self,size):
		assert size > 0, "Array size must be > 0"
		self.size = size
		PyArray = ctypes.py_object * size
		self.elements = PyArray()
		self.clear(None)
	def __len__(self):
		return self.size
	def __getitem__(self,index):
		assert index >= 0 and index < len(self), "Illegal index"
		return self.elements[index]
	def __setitem__(self,index,item):
		assert index >= 0 and index < len(self), "Illegal index"
		self.elements[index] = item
	def clear(self,value):
		for i in range(len(self)):
			self.elements[i] = value
	def __iter__(self):
		return arrayIter(self,self.elements)
		
class arrayIter:
	def __init__(self,theArray):
		self.array = theArray
		self.index = 0
	def __iter__(self):
		return self
	def __next__(self):
		if self.index < len(self.array):
			item = self.array[self.index]
			self.index += 1
			return item
		else:
			raise StopIteration
class myArray2D(array):
	def  __init__(self,nRows,nCols):
		array.__init__(self,nRows * nCols)
		self.nRows = nRows
		self.nCols = nCols
	def __getitem__(self,indexTuple):
		assert len(indexTuple) == 2, "Illegal Index"
		row = indexTuple[0]
		col = indexTuple[1]
		assert row >= 0 and row < self.nRows \
			and col >= 0 and col < self.nCols,\
				"Illegal Index"
		index = row * self.nCols + col
		return array.__getitem__(self,index)
	def __setitem__(self,indexTuple,item):
		assert len(indexTuple) == 2, "Illegal Index"
		row = indexTuple[0]
		col = indexTuple[1]
		assert row >= 0 and row < self.nRows \
			and col >= 0 and col < self.nCols,\
				"Illegal Index"
		index = row * self.nCols + col
		array.__setitem__(self,index,item)
class array2D:
	def __init__(self,nRows,nCols):
		self.nRows = nRows
		self.nCols = nCols
		self.rows = array(nRows)
		for i in range(nRows):
			self.rows[i] = array(nCols)
	def numOfRows(self):
		return self.nRows
	def numOfCols(self):
		return self.nCols
	def __getitem__(self,indexTuple):
		assert len(indexTuple) == 2, "Illegal Index"
		row = indexTuple[0]
		col = indexTuple[1]
		assert row >= 0 and row < self.nRows \
			and col >= 0 and col < self.nCols,\
				"Illegal Index"
		theArray = self.rows[row]
		return theArray[col]
	def __setitem__(self,indexTuple,item):
		assert len(indexTuple) == 2, "Illegal Index"
		row = indexTuple[0]
		col = indexTuple[1]
		assert row >= 0 and row < self.nRows \
			and col >= 0 and col < self.nCols,\
				"Illegal Index"
		theArray = self.rows[row]
		theArray[col] = item 
a = array(10)
for i in range(10):
	a[i] = 2**i
	print a[i]
aa = myArray2D(5):
		aa[i,j] = i * j
		print(a[i])
