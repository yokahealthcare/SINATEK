import numpy as np
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