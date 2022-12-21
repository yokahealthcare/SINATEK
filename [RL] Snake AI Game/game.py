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
SPEED = 20

class SnakeGame:
	def __init__(self, w=640, h=480):
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

		# check if the food inside the snake
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

	def _is_collision(self):
		x = self.head.x
		y = self.head.y
		if x > self.w-BLOCK_SIZE or x < 0 or y > self.h-BLOCK_SIZE or y < 0 or self.head in self.body[1:]:
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

	def _update_ui(self):
		self.display.fill(BLACK)
		        
		for pt in self.body:
			pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
			# pygame.draw.rect(self.display, RED, pygame.Rect(pt.x+4, pt.y, 12, 12))
		            
		pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
		        
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