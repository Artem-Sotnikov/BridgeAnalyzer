import numpy as np

class Layer:
	def __init__(self, prev_size, own_size):
		self.w = np.random.rand(own_size, prev_size) - .5
		self.b = np.random.rand(own_size) - .5
		self.a = np.zeros(own_size)
	def activate(self, prev):
		# using relu
		self.a = self.w @ prev.a + self.b
		np.maximum(self.a, 0, self.a)

class NN:
	layers = []
	last_size = 0
	def add_layer(self, size):
		# the first layer is just input
		if not self.last_size:
			self.layers.append(Layer(1, size))
			self.last_size = size
		else:
			self.layers.append(Layer(self.last_size, size))
			self.last_size = size
	def compute(self, inp):
		self.layers[0].a = inp
		for i, a in enumerate(self.layers):
			if i == len(self.layers)-1:
				break
			self.layers[i+1].activate(a)

if __name__ == '__main__':
	# unit test successful
	ha = NN()
	ha.add_layer(3)
	ha.add_layer(2)
	print(ha.layers[1].w, '\n')
	print(ha.layers[1].b, '\n')
	ha.compute(np.array([2 for i in range(3)]))
	print(ha.layers[1].a)
