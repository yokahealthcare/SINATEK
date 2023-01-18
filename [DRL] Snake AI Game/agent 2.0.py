import torch
import random
import numpy as np
from collections import deque
from gameAI import SnakeGameAI
from Brain import Linear_QNet
from Dqn import QTrainer
import os, time

from graph import plot

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

env = SnakeGameAI(w=640, h=480, isDisplayed=True)

class Agent:
	def __init__(self):
		self.n_games = 0
		self.total_score = 0
		self.epsilon = 0 # randomness
		self.discount = 0.99 # discount rate
		self.memory = deque(maxlen=MAX_MEMORY)
		self.model = Linear_QNet(15, 256, 3)
		self.trainer = QTrainer(self.model, LR, self.discount)

	def remember(self, current_state, action, reward, next_state, game_over):
		self.memory.append((current_state, action, reward, next_state, game_over))

	def train_short_memory(self, current_state, action, reward, next_state, game_over):
		self.trainer.train_step(current_state, action, reward, next_state, game_over)

	def train_long_memory(self):
		if len(self.memory) > BATCH_SIZE:
			# Pick random 1000 data
			data = random.sample(self.memory, BATCH_SIZE)
		else:
			# If it less than 1000 data
			data = self.memory

		# unzip the data
		current_states, actions, rewards, next_states, game_overs = zip(*data)

		self.trainer.train_step(current_states, actions, rewards, next_states, game_overs)
	
	def get_action(self, state):
		# random moves: tradeoff exploration / exploitation
		self.epsilon = 80 - self.n_games
		if self.epsilon <= 0:
			self.epsilon = 1 		# SETTING THE MIN. EXPLORATION VALUE
		final_move = [0,0,0]
		if random.randint(0, 200) < self.epsilon:
			move = random.randint(0, 2)
			final_move[move] = 1
		else:
			state0 = torch.tensor(state, dtype=torch.float)
			prediction = self.model(state0)
			move = torch.argmax(prediction).item()
			final_move[move] = 1

		return final_move

	def show_debug_information(self, episode, current_state, action, reward, next_state, game_over, score):
		print("EPISODE : {}".format(episode))
		print("---------- Game Debug Information ----------")
		print("Score \t\t: {}".format(score))
		print("Epsilon \t: {}".format(self.epsilon))

		print("---------- State Debug Information ----------")
		print("Current State \t: {}".format(current_state))
		print("Action \t\t: {}".format(action))
		print("Reward \t\t: {}".format(reward))
		print("Next State \t: {}".format(next_state))
		print("Game Over \t: {}".format(game_over))

		print("---------- Memory Debug Information ----------")	
		print("Memory Length : {}".format(len(self.memory)))
		# print("Memory Content:")
		# print(self.memory)

		print()


	"""
	LESSON THAT I GATHERED:
	1. ALWAYS HAVING ENVIRONMENT DATA (ex. state, action) ON NUMPY ARRAY  (CATEGORICAL DATA)
	2. DEEP LEARNING WILL BROKE IF IT DISCRETE

	"""

	def run(self):
		plot_scores = []
		plot_mean_scores = []
		record = 0
		
		while True:
			current_state = env.get_state()

			# Getting action
			action = self.get_action(current_state)

			# Playing the game
			next_state, reward, game_over, score = env.play_step(action)

			# Train short memory
			self.train_short_memory(current_state, action, reward, next_state, game_over)

			# Remember it
			self.remember(current_state, action, reward, next_state, game_over)
		
			if game_over:
				# Train Long Memory
				self.train_long_memory()

				# Showing debug data
				self.show_debug_information(self.n_games, current_state, action, reward, next_state, game_over, score)
				
				self.n_games += 1
				env.gen = self.n_games
				
				if score > record:
					record = score
					self.model.save()

				plot_scores.append(score)
				plot_mean_scores.append(score/self.n_games)
				plot(plot_scores, plot_mean_scores)
				env.reset()

if __name__ == '__main__':
	agent1 = Agent()
	agent1.run()



