import tensorflow as tf
import numpy as np

class Layer:
    def __init__(self, inputCount, outputCount):
        self.inputCount = inputCount
        self.outputCount = outputCount
        self.weights = 0.10 * np.random.randn(inputCount, outputCount)
        self.biases = np.zeros((1, outputCount))

	def forward(self, inputs):
		self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLU:
	def forward(self, inputs):
		self.output = np.maximum(0, inputs)


class Activation_Softmax:
	def forward(self, inputs):
		# Get unnormalized probabilities
		exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
		# Normalize for each sample
		probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)

		self.output = probabilities

