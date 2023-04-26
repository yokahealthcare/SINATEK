import numpy as np
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
