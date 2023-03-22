import numpy as np


"""
import tensorflow as tf
class Dqn:
	def __init__(self, max_memory, discount):
		self.max_memory = max_memory
		self.discount = discount
		self.memory = list()

	def remember(self, transition, game_over):
		self.memory.append([transition, game_over])
		if len(self.memory) > self.max_memory:
			del self.memory[0]

	def getBatches(self, model, batch_size):
		len_memory = len(self.memory)
		numInputs = self.memory[0][0][0].shape[1] 		# STATE SPACES
		numOutputs = model.output_shape[-1]				# ACTION SPACES

		inputs = np.zeros((min(batch_size, len_memory), numInputs))
		targets = np.zeros((min(batch_size, len_memory), numOutputs))

		# Extraction
		for i, inx in enumerate(np.random.randint(0, len_memory, size=min(batch_size, len_memory))):
			current_state, action, reward, next_state = self.memory[inx][0]
			game_over = self.memory[inx][1]

			inputs[i] = current_state
			targets[i] = model.predict(current_state)[0]
			if game_over:
				targets[i][action] = reward			# ??????????
			else:
				targets[i][action] = reward + self.discount * np.max(model.predict(next_state)[0])

		return inputs, targets

"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()



