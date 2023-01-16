import pygame
import random
import numpy as np
import os
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('Cascadia Mono', 25)

class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4

Point = namedtuple('Point', 'x, y')

# COLORS
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (37, 37, 37)
DARK_GREEN = (26, 77, 46)
ORANGE = (255, 159, 41)

# GAME CONFIGURATION
BLOCK_SIZE = 20

class SnakeGameAI:
	def __init__(self, w=400, h=400, isDisplayed=False):
		self.w = w
		self.h = h
		self.isDisplayed = isDisplayed
		self.gen = 0

		self.observation_space = (11, )
		self.action_space = 3

		# INITILAZATION
		self.SPEED = 70
		if self.isDisplayed:
			self.display = pygame.display.set_mode((self.w, self.h))
			pygame.display.set_caption('Snake Game AI')
			self.SPEED = 40
		self.clock = pygame.time.Clock()

		self.reset()
		
	def reset(self):
		# DEFAULT GAME STATE
		self.direction = Direction.RIGHT
		self.head = Point(self.w/2, self.h/2)
		self.body = [
			self.head, 										# HEAD
			Point(self.head.x-BLOCK_SIZE, self.head.y),		# TAIL 1
			Point(self.head.x-BLOCK_SIZE*2, self.head.y)	# TAIL 2
		]
		self.score = 0
		self.frame_iteration = 0
		self.food = None
		self._place_food()
		

	def _place_food(self):
		x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
		y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
		self.food = Point(x,y)

		# check if the food inside the snake
		if self.food in self.body:
			self._place_food()

	def play_step(self, action):
		self.frame_iteration += 1
		gameOver = False
		reward = 0 				# DEFAULT REWARD IF NOTHING HAPPEN

		# EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True

		# MOVING
		self._move(action)
		self.body.insert(0, self.head)

		# EAT
		if self.head == self.food:
			self.score += 1
			reward = 10
			self._place_food()
		else:
			self.body.pop()

		# COLLISION
		if self._is_collision() or self.frame_iteration > (100*len(self.body)):
			gameOver = True
			reward = -10
			return self.get_state(), reward, gameOver, self.score

		# UPDATE UI
		self._update_ui()
		self.clock.tick(self.SPEED)

		return self.get_state(), reward, gameOver, self.score

	def _is_collision(self, p=None):
		if p == None:
			p = self.head

		x = p.x
		y = p.y
		if x > self.w-BLOCK_SIZE or x < 0 or y > self.h-BLOCK_SIZE or y < 0:
			return True
    	
		if p in self.body[1:]:
			return True

		return False

	def _move(self, action):
		# [straight, right, left]
		clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
		idx = clock_wise.index(self.direction)

		if np.array_equal(action, [1, 0, 0]):
			new_dir = clock_wise[idx] # no change
		elif np.array_equal(action, [0, 1, 0]):
			next_idx = (idx + 1) % 4
			new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
		else: 
			next_idx = (idx - 1) % 4
			new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

		self.direction = new_dir

		x = self.head.x
		y = self.head.y

		if self.direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif self.direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif self.direction == Direction.UP:
			y -= BLOCK_SIZE
		elif self.direction == Direction.DOWN:
			y += BLOCK_SIZE

		self.head = Point(x,y)

	
	"""
	-------------------- ACTION
	[1, 0, 0]       : straight
	[0, 1, 0]       : right turn
	[0, 0, 1]       : left turn
	-------------------- REWARD
	Eat Food        : +10
	Game Over       : -10
	Else            : 0
	-------------------- STATE (11 values)
	[
	    danger straight, danger right, danger left,
	    danger left corner, danger right corner,
	    
	    direction left, direction right,
	    direction up, direction down,
	    	
	    food left, food right,
	    food up, food down
	]

	"""
	
	def get_state(self):
		coll_l = Point(self.head.x-BLOCK_SIZE, self.head.y)
		coll_r = Point(self.head.x+BLOCK_SIZE, self.head.y)	
		coll_u = Point(self.head.x, self.head.y-BLOCK_SIZE)
		coll_d = Point(self.head.x, self.head.y+BLOCK_SIZE)

		coll_lcu = Point(self.head.x-BLOCK_SIZE, self.head.y-BLOCK_SIZE)
		coll_rcu = Point(self.head.x+BLOCK_SIZE, self.head.y-BLOCK_SIZE)
		coll_lcd = Point(self.head.x-BLOCK_SIZE, self.head.y+BLOCK_SIZE)
		coll_rcd = Point(self.head.x+BLOCK_SIZE, self.head.y+BLOCK_SIZE)

		dir_l = self.direction == Direction.LEFT
		dir_r = self.direction == Direction.RIGHT
		dir_u = self.direction == Direction.UP
		dir_d = self.direction == Direction.DOWN

		states = [
		
			# DANGER
			# STRAIGHT
			((dir_u and self._is_collision(coll_u)) or
			(dir_r and self._is_collision(coll_r)) or
			(dir_d and self._is_collision(coll_d)) or
			(dir_l and self._is_collision(coll_l))),

			# RIGHT
			((dir_u and self._is_collision(coll_r)) or
			(dir_r and self._is_collision(coll_d)) or
			(dir_d and self._is_collision(coll_l)) or
			(dir_l and self._is_collision(coll_u))),

			# LEFT
			((dir_u and self._is_collision(coll_l)) or
			(dir_r and self._is_collision(coll_u)) or
			(dir_d and self._is_collision(coll_r)) or
			(dir_l and self._is_collision(coll_d))),

			# LEFT CORNER
			((dir_u and self._is_collision(coll_lcu)) or
			(dir_r and self._is_collision(coll_rcu)) or
			(dir_d and self._is_collision(coll_rcd)) or
			(dir_l and self._is_collision(coll_lcd))),

			# RIGHT CORNER
			((dir_u and self._is_collision(coll_rcu)) or
			(dir_r and self._is_collision(coll_rcd)) or
			(dir_d and self._is_collision(coll_lcd)) or
			(dir_l and self._is_collision(coll_lcu))),

			dir_l,
			dir_r,
			dir_u,
			dir_d,

			self.food.x < self.head.x,  # food left
	        self.food.x > self.head.x,  # food right
	        self.food.y < self.head.y,  # food up
	        self.food.y > self.head.y  # food down
		]

		"""
		# Returned Boolean Tuple. ex. (False, True, False, ...)
		#boolean_tuple = tuple(states)

		# We need to converted to Integer Tuple
		#integer_tuple = tuple([i*1 for i in boolean_tuple])
		
		"""

		# Make it numpy 2D array
		#return np.array(np.reshape(states, (1, len(states))), dtype=int)			 

		# Make it numpy 1D array
		return np.array(states, dtype=int)

	def show_debug_states(self, states):
		os.system("cls")
		print("======== STATES ============ ")
		print("-- DANGER")
		print("STRAIGHT : {}\tRIGHT : {}\tLEFT : {}\tL.CORNER : {}\tR.CORNER :{}".format(states[0], states[1], states[2], states[3], states[4]))
		print("-- DIRECTION")
		print("LEFT : {}\tRIGHT : {}\tUP : {}\tDOWN : {}".format(states[5], states[6], states[7], states[8]))
		print("-- FOOD")
		print("LEFT : {}\tRIGHT : {}\tUP : {}\tDOWN : {}".format(states[9], states[10], states[11], states[12]))

	def _update_ui(self):
		if self.isDisplayed:
			self.display.fill(BLACK)
			        
			for inx, pt in enumerate(self.body):
				if inx == 0:
					# HEAD
					pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
				else:
					# BODY
					pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
					#pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x+0.5, pt.y+0.5, BLOCK_SIZE-0.5, BLOCK_SIZE-0.5))
			            
			pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

			text = font.render("Score: " + str(self.score), True, WHITE)
			self.display.blit(text, [0, 30])

			text = font.render("Gen: " + str(self.gen), True, WHITE)
			self.display.blit(text, [0, 0])

			pygame.display.flip()