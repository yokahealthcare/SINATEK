#!usr/bin/env python
from game import SnakeGame
from queue import PriorityQueue

class State(object):
	def __init__(self, value, parent, start=0, goal=0, solver=0):
		self.children = []
		self.parent = parent
		self.value = value
		self.dist = 0

		if parent:
			self.path = parent.path[:]
			self.path.append(value)
			self.start = parent.start
			self.goal = parent.goal
			self.solver = parent.solver
		else:
			self.path = [value]
			self.start = start
			self.goal = goal
			self.solver = solver

	def getDist(self):
		pass

	def createChildren(self):
		pass

class State_String(State):
	def __init__ (self, value, parent, start=0, goal=0):
		super(State_String, self).__init__(value, parent, start, goal)
		self.dist = self.getDist()

	def getDist(self):
		# if goal reached return 0
		if self.value == self.goal:
			return 0

		dist = 0
		for i in range(len(self.goal)):
			letter = self.goal[i]
			dist += abs(i - self.value.index(letter))
		return dist

	def createChildren(self):
		if not self.children:
			for i in xrange(len(self.goal)-1):
				val = self.value
				val = val[:i] + val[i+1] + val[i] + val[i+2:]
				child = State_String(val, self)
				self.children.append(child)

class AStar_Solver:
	def __init__(self, start, goal):
		self.path = [] 					# will be filled with path to the goal
		self.visitedQueue = []
		self.priorityQueue = PriorityQueue()
		self.start = start
		self.goal = goal

	def solve(self):
		startState = State_String(self.start, 0, self.start, self.goal)

		count = 0
		self.priorityQueue.put((0, count, startState)) # put a tuple; 0 is the index at priority queue
		while(not self.path and self.priorityQueue.qsize()):
			closestChild = self.priorityQueue.get()[2] # get the 'startState' variable
			closestChild.createChildren()
			self.visitedQueue.append(closestChild.value)

			for child in closestChild.children:
				if child.value not in self.visitedQueue:
					count += 1
					if not child.dist:
						self.path = child.set_path
						break
					self.priorityQueue.put((child.dist, count, child))

		if not self.path:
			print("Goal of {} is not possible!".format(self.goal))
		return self.path


if __name__ == '__main__':

	start1 = "hma"
	goal1 = "abcdef"
	print("starting...")
	a = AStar_Solver(start1, goal1)
	a.solve()

	for i in xrange(len(a.path)):
		print("{}) {}".format(i, a.path[i]))


	"""
	game = SnakeGame()

	while True:
		game_over, score = game.play_step()

		head_x, head_y, food_x, food_y = game.get_state()



		if game_over:
			break
	"""
