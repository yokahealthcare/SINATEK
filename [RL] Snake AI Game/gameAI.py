import pygame
import random
from enum import Enum
from collections import namedtuple

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

# GAME CONFIGURATION
BLOCK_SIZE = 20
SPEED = 2

# JUST PLAYING...
list_of_apples = list()
for i in range(100):
	x = random.randint(0, 9) * BLOCK_SIZE
	y = random.randint(0, 9) * BLOCK_SIZE
	list_of_apples.append([x, y])

class SnakeGameAI:
	def __init__(self, w=200, h=200):
		self.w = w
		self.h = h

		# INITILAZATION
		self.display = pygame.display.set_mode((self.w, self.h))
		pygame.display.set_caption('Snake Game AI')
		self.clock = pygame.time.Clock()

		# POSSIBLE TILE
		self.possible_x = (self.w - BLOCK_SIZE) // BLOCK_SIZE
		self.possible_y = (self.h - BLOCK_SIZE) // BLOCK_SIZE

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
		self.food = None
		self.index_apple = 0
		self._place_food()
		self.frame_iteration = 0
		self.state = int((self.possible_x * self.head.y + self.head.x) / 20)
		


	def _place_food(self):
		#x = random.randint(0, self.possible_x) * BLOCK_SIZE
		#y = random.randint(0, self.possible_y) * BLOCK_SIZE
		x = list_of_apples[self.index_apple][0]
		y = list_of_apples[self.index_apple][1]
		self.food = Point(x,y)

		# check if the food inside the snake
		if self.food in self.body:
			self._place_food()

		self.index_apple += 1

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
		if self._is_collision() or self.frame_iteration > 100 * len(self.body):
			gameOver = True
			reward = -10
			return self.state, reward, gameOver, self.score

		# UPDATE UI
		self._update_ui()
		self.clock.tick(SPEED)

		return self.state, reward, gameOver, self.score

	def _is_collision(self):
		x = self.head.x
		y = self.head.y
		if x > self.w-BLOCK_SIZE or x < 0 or y > self.h-BLOCK_SIZE or y < 0 or self.head in self.body[1:]:
			return True
    	
		return False

	def _move(self, action):
		
		clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
		idx = clock_wise.index(self.direction)

		if action == 0:
			new_dir = clock_wise[idx] # no change
		elif action == 1:
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
		self.state = int((self.possible_x * self.head.y + self.head.x) / 20)
	

	def _update_ui(self):
		self.display.fill(BLACK)
		        
		for pt in self.body:
			pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
			# pygame.draw.rect(self.display, RED, pygame.Rect(pt.x+4, pt.y, 12, 12))
		            
		pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
		
		print("STATE : {}".format(self.state))

		text = font.render("Score: " + str(self.score), True, WHITE)
		self.display.blit(text, [0, 0])
		pygame.display.flip()


if __name__ == '__main__':
	action = 0
	# THIS will make the SNAKE LOOPING to the RIGHT
	

	game = SnakeGameAI()
	while True:
		# EVENTS
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					action = 1
				if event.key == pygame.K_LEFT:
					action = 2
		state, reward, gameOver, score = game.play_step(action)
		action = 0

		if gameOver:
			game.reset()

	print("THANK YOU FOR PLAYING!")
	print('Final Score : {}'.format(game.score))

	pygame.quit()