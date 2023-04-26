import pygame
from pygame import gfxdraw
import random
import numpy as np
import os
from enum import Enum
from collections import namedtuple
from collections import deque

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4

Point = namedtuple('Point', 'x, y')

# COLORS
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (0,255,0)

# GAME CONFIGURATION
BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
	def __init__(self, w=400, h=400):
		self.w = w
		self.h = h

		# INITILAZATION
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption('Snake')
		self.clock = pygame.time.Clock()

		# DEFAULT GAME STATE
		self.direction = Direction.RIGHT
		self.head = Point(self.w/2, self.h/2)
		self.body = [
			self.head, 										# HEAD
			Point(self.head.x-BLOCK_SIZE, self.head.y),		# TAIL 1
			Point(self.head.x-BLOCK_SIZE*2, self.head.y)	# TAIL 2
		]
		self.score = 0
		self.food = None
		self._place_food()

	def _place_food(self):
		x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
		y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
		self.food = Point(x,y)

		# check if the food inside the snake, then placed new food
		if self.food in self.body:
			self._place_food()

	def play_step(self):
		gameOver = False

		# EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
					self.direction = Direction.RIGHT
				if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
					self.direction = Direction.LEFT
				if event.key == pygame.K_UP and self.direction != Direction.DOWN:
					self.direction = Direction.UP
				if event.key == pygame.K_DOWN and self.direction != Direction.UP:
					self.direction = Direction.DOWN

		# MOVING
		self._move(self.direction)
		self.body.insert(0, self.head)

		# EAT
		if self.head == self.food:
			self.score += 1
			self._place_food()
		else:
			self.body.pop()

		# COLLISION
		if self._is_collision():
			gameOver = True
			return gameOver, self.score

		# UPDATE UI
		self._update_ui()
		self.clock.tick(SPEED)

		return gameOver, self.score

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

	def _move(self, direction):
		x = self.head.x
		y = self.head.y

		if direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif direction == Direction.UP:
			y -= BLOCK_SIZE
		elif direction == Direction.DOWN:
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
	-------------------- STATE (47 values)
	[
	    danger straight, danger right, danger left,
	    danger front left corner, danger front right corner,
	    danget back left corner, danger back right corner,
	    
	    direction left, direction right,
	    direction up, direction down,
	    	
	    food left, food right,
	    food up, food down,

	    danger all way up (8), danger all way down(8 digits),
	    danger all way left (8), danger all way right (8)
	]

	"""

	def decimal_to_binary(self, decimal):
		binary = bin(decimal).replace("0b", "")
		binary = "{}{}".format((8 - len(binary))*'0', binary)
		return list(binary)

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

		dist_to_wall_u = int(self.head.y / BLOCK_SIZE)
		dist_to_wall_d = int((self.h-self.head.y-BLOCK_SIZE) / BLOCK_SIZE)
		dist_to_wall_l = int(self.head.x / BLOCK_SIZE)
		dist_to_wall_r = int((self.w-self.head.x-BLOCK_SIZE) / BLOCK_SIZE)

		danger_dist_u = None
		danger_dist_d = None
		danger_dist_l = None
		danger_dist_r = None

		# UP CHECKER
		for i in range(dist_to_wall_u+1):
			tmp_point = Point(self.head.x, self.head.y-(i+1)*BLOCK_SIZE)
			if i <= dist_to_wall_u and tmp_point in self.body[1:] and not dir_d:
				# body collision
				danger_dist_u = int((self.head.y - tmp_point.y - BLOCK_SIZE) / BLOCK_SIZE)
				break
			elif i == dist_to_wall_u:
				# wall collision
				danger_dist_u = i

			pygame.gfxdraw.pixel(self.display, int(tmp_point.x)+10, int(tmp_point.y), GREEN)

		# DOWN CHECKER
		for i in range(dist_to_wall_d+1):
			tmp_point = Point(self.head.x, self.head.y+(i+1)*BLOCK_SIZE)
			if i <= dist_to_wall_d and tmp_point in self.body[1:] and not dir_u:
				# body collision
				danger_dist_d = int((tmp_point.y - self.head.y - BLOCK_SIZE) / BLOCK_SIZE)
				break
			elif i == dist_to_wall_d:
				# wall collision
				danger_dist_d = i

			pygame.gfxdraw.pixel(self.display, int(tmp_point.x)+10, int(tmp_point.y), GREEN)


		# LEFT CHECKER
		for i in range(dist_to_wall_l+1):
			tmp_point = Point(self.head.x-(i+1)*BLOCK_SIZE, self.head.y)
			if i <= dist_to_wall_l and tmp_point in self.body[1:] and not dir_r:
				# body collision
				danger_dist_l = int((self.head.x - tmp_point.x - BLOCK_SIZE) / BLOCK_SIZE)
				break
			elif i == dist_to_wall_l:
				# wall collision
				danger_dist_l = i

			pygame.gfxdraw.pixel(self.display, int(tmp_point.x), int(tmp_point.y)+10, GREEN)

		# RIGHT CHECKER
		for i in range(dist_to_wall_r+1):
			tmp_point = Point(self.head.x+(i+1)*BLOCK_SIZE, self.head.y)
			if i <= dist_to_wall_r and tmp_point in self.body[1:] and not dir_l:
				# body collision
				danger_dist_r = int((tmp_point.x - self.head.x - BLOCK_SIZE) / BLOCK_SIZE)
				break
			elif i == dist_to_wall_r:
				# wall collision
				danger_dist_r = i

			pygame.gfxdraw.pixel(self.display, int(tmp_point.x), int(tmp_point.y)+10, GREEN)


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

			# FRONT LEFT CORNER
			((dir_u and self._is_collision(coll_lcu)) or
			(dir_r and self._is_collision(coll_rcu)) or
			(dir_d and self._is_collision(coll_rcd)) or
			(dir_l and self._is_collision(coll_lcd))),

			# FRONT RIGHT CORNER
			((dir_u and self._is_collision(coll_rcu)) or
			(dir_r and self._is_collision(coll_rcd)) or
			(dir_d and self._is_collision(coll_lcd)) or
			(dir_l and self._is_collision(coll_lcu))),

			# BACK LEFT CORNER
			((dir_u and self._is_collision(coll_lcd)) or
			(dir_r and self._is_collision(coll_lcu)) or
			(dir_d and self._is_collision(coll_rcu)) or
			(dir_l and self._is_collision(coll_rcd))),

			# BACK RIGHT CORNER
			((dir_u and self._is_collision(coll_rcd)) or
			(dir_r and self._is_collision(coll_lcd)) or
			(dir_d and self._is_collision(coll_lcu)) or
			(dir_l and self._is_collision(coll_rcu))),

			dir_l,
			dir_r,
			dir_u,
			dir_d,

			self.food.x < self.head.x,  # food left
	        self.food.x > self.head.x,  # food right
	        self.food.y < self.head.y,  # food up
	        self.food.y > self.head.y  # food down

		]

		for i in self.decimal_to_binary(danger_dist_u):
			states.append(i)
		for i in self.decimal_to_binary(danger_dist_d):
			states.append(i)
		for i in self.decimal_to_binary(danger_dist_l):
			states.append(i)
		for i in self.decimal_to_binary(danger_dist_r):
			states.append(i)

		return np.array(states, dtype=int)

	def show_debug_states(self, states):
		os.system("cls")
		print("======== STATES ============ ")
		print("-- DANGER")
		print("STRAIGHT : {}\tRIGHT : {}\tLEFT : {}\nLF.CORNER : {}\tRF.CORNER :{}\tLD.CORNER : {}\tRD.CORNER :{}".format(states[0], states[1], states[2], states[3], states[4], states[5], states[6]))
		print("-- DIRECTION")
		print("LEFT : {}\tRIGHT : {}\tUP : {}\tDOWN : {}".format(states[7], states[8], states[9], states[10]))
		print("-- FOOD")
		print("LEFT : {}\tRIGHT : {}\tUP : {}\tDOWN : {}".format(states[11], states[12], states[13], states[14]))

	def _update_ui(self):
		self.display.fill(BLACK)
		        
		for pt in self.body:
			pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
		            
		pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

		#self.show_debug_states(self.get_state())
		os.system("cls")
		states_val = self.get_state()
		print("STATE LENGTH : {}\n STATE : {}".format(len(states_val), states_val))

		text = font.render("Score: " + str(self.score), True, WHITE)
		self.display.blit(text, [0, 0])
		pygame.display.flip()


if __name__ == '__main__':

	game = SnakeGame()
	while True:
		gameOver, score = game.play_step()

		if gameOver:
			break

	print("THANK YOU FOR PLAYING!")
	print('Final Score : {}'.format(game.score))

	pygame.quit()