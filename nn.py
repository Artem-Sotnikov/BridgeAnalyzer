'''created by Stephen Wang'''

import numpy as np
from copy import deepcopy as dcp

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

	def __init__(self, config=None):
		# config is a one-dimensional iterable whose elements are layer sizes in order (L->R)
		for i in config:
			self.add_layer(i)

	def compute(self, inp):
		self.layers[0].a = inp
		for i, a in enumerate(self.layers):
			if i == len(self.layers)-1:
				break
			self.layers[i+1].activate(a)
		return self.layers[-1].a

	def get_output(self):
		return self.layers[-1].a

class Member(NN):
	def __init__(self, config=None):
		super().__init__(config)
		self.truss = []
	
	def compute(self, inp):
		super().compute(inp)
		# overloaded compute will run the nn the specified number of times to produce every member/joint in the truss

class GeneticAlgorithm:
	def __init__(self, member, population_size, mutation_factor):
		self.population = np.array([member for _ in range(population_size)])
		self.transition_pop = dcp(self.population)
		self.population_size = population_size
		self.mutation_factor = mutation_factor
		self.generation = 0
		self.pop_fitness = np.zeors(population_size)

	def perform(self):
		for i, a in enumerate(self.population):
			size = self.population[0].layers[0].a.shape[0]
			self.pop_fitness[i] = a.compute(np.zeros(size))

	def compute_fitness(self):
		pass

	def normalize_fitness(self):
		max_ = self.pop_fitness.max()
		min_ = self.pop_fitness.min()
		range_ = max_ - min_
		self.pop_fitness = (self.pop_fitness-min_)/range_

	def reproduce(self):
		self.normalize_fitness()
		for i, a in enumerate(self.population):
			# each individual from the population
			for b in self.population:
				# tries to find a mate in the population
				if np.random.random() > self.pop_fitness[i]:
					# mating + mutation happens here
					break

	def evolve(self):
		pass

if __name__ == '__main__':
	# unit test successful
	ha = NN()
	ha.add_layer(3)
	ha.add_layer(2)
	print(ha.layers[1].w, '\n')
	print(ha.layers[1].b, '\n')
	ha.compute(np.array([2 for i in range(3)]))
	print(ha.layers[1].a)
