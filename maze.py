class Stack():
	""" This class purpose is to append data to self.elems """
	def __init__(self):
		self.elems = [ ]
	def is_empty(self):
		return self.elems == [ ]
	def top(self):
		if self.elems == [ ]:
			raise StackUnderflow
		return self.elems[len(self.elems)-1]
	def push(self, elem):
		self.elems.append(elem)
	def pop(self):
		if self.elems == [ ]:
			raise StackUnderflow
		return self.elems.pop()
		
		
class element():
	""" This class purpose is to initialize data and assigning them """
	def __init__(self,x,y,status):
		self.x = x
		self.y = y
		self.s = status
		
directions = ((0,1),(1,0),(0,-1),(-1,0))
maze = [[1,1,1,1,1,1],[1,0,1,0,1,1],[1,0,0,0,0,1],[1,0,1,0,1,1],[1,1,1,1,1,1]]
def mazePath (maze,x,y,end_x,end_y):
	""" This function runs the algorithm of the maze.py """
	st = Stack()
	maze[x][y] = 2
	ele = element(x,y,-1)
	st.push(ele)
	while not st.is_empty():
		top = st.top()
		#print ("(%d,%d)"%(top.x,top.y))
		while top.s < 3:
			top = st.top()
			top.s += 1
			new_x, new_y = top.x + directions[top.s][0], top.y + directions[top.s][1]
			if (new_x, new_y) == (end_x, end_y):
				print (new_x," ",new_y)
				while not st.is_empty() :
					ele = st.pop()
					print (ele.x," ",ele.y)
				return True
			if maze[new_x][new_y] == 0 :
				newele = element(new_x,new_y,-1)
				maze[new_x][new_y] = 2
				st.push(newele)
				continue 
		st.pop()
	print ("No way")
	return False
# This will run the whole script	
mazePath(maze,1,1,3,3)
