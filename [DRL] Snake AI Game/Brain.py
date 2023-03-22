import numpy as np

"""
import tensorflow as tf
class Brain:
	def __init__(self, numInputs, numOutputs, lr=0.001):
		self.numInputs = numInputs
		self.numOutputs = numOutputs
		self.lr = lr

	def model(self):
		model = tf.keras.models.Sequential()
		model.add(tf.keras.layers.Dense(32, activation='relu', input_shape=(self.numInputs, )))
		model.add(tf.keras.layers.Dense(16, activation='relu'))
		model.add(tf.keras.layers.Dense(self.numOutputs, activation='softmax'))

		model.compile(optimizer=tf.keras.optimizers.Adam(lr=self.lr), loss=tf.keras.losses.Huber(), metrics=['accuracy'])

		return model
"""
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size1, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size1)
        self.linear2 = nn.Linear(hidden_size1, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)