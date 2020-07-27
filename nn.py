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
		self.layers = []
		self.last_size = 0
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
		return super().compute(inp)
		# overloaded compute will run the nn the specified number of times to produce every member/joint in the truss

class GeneticAlgorithm:
	def __init__(self, conf, population_size, mutation_factor):
		self.population = np.array([Member(config=conf) for _ in range(population_size)])
		self.transition_pop = dcp(self.population)
		self.population_size = population_size
		self.mutation_factor = mutation_factor
		self.generation = 0
		self.pop_fitness = np.zeros(population_size)

	def perform(self):
		for i, a in enumerate(self.population):
			size = self.population[0].layers[0].a.shape
			# change this step for different architectures/approaches
			self.pop_fitness[i] = a.compute(np.random.random(size)-.5)
			# self.pop_fitness[i] = a.compute(np.ones(3))

	def compute_fitness(self):
		# test case of just a simple quadratic function
		for i, a in enumerate(self.population):
			self.pop_fitness[i] = (a.get_output().sum() - a.layers[0].a[0] - a.layers[0].a[1] * 5 - a.layers[0].a[2] * .5)**-2*5
		print(self.pop_fitness)

	def normalize_fitness(self):
		max_ = self.pop_fitness.max()
		min_ = self.pop_fitness.min()
		range_ = max_ - min_
		self.pop_fitness = (self.pop_fitness-min_)/range_

	def reproduce(self):
		self.normalize_fitness()
		for i, a in enumerate(self.population):
			# each individual from the population
			for j, b in enumerate(self.population):
				# tries to find a mate in the population
				# if np.random.random() > self.pop_fitness[i]:
				if self.pop_fitness[j] > 0.95:
					# mating + mutation happens here
					self.transition_pop[i] = dcp(a)
					for c in range(len(a.layers)):
						gene = np.random.random(a.layers[c].w.shape) - .5
						self.transition_pop[i].layers[c].w = a.layers[c].w*(gene>=0) + b.layers[c].w*(gene<0) + gene*(np.random.random(a.layers[c].w.shape)-.6>0)*self.mutation_factor
						gene = np.random.random(a.layers[c].b.shape) - .5
						self.transition_pop[i].layers[c].b = a.layers[c].b*(gene>=0) + b.layers[c].b*(gene<0) + gene*(np.random.random(a.layers[c].b.shape)-.6>0)*self.mutation_factor
					break
		self.population = dcp(self.transition_pop)

	def evolve(self):
		self.perform()
		self.compute_fitness()
		self.reproduce()
		self.generation += 1
		print(self.test(np.ones(3)))

	def test(self, inp):
		temp_ind, temp_score = 0, 0
		for i, a in enumerate(self.pop_fitness):
			if a > temp_score:
				temp_ind, temp_score = i, a
		huh = self.population[temp_ind]
		return huh.compute(inp)

if __name__ == '__main__':
	test = GeneticAlgorithm([3,1], 20, 2)
	for i in range(100):
		test.evolve()
	# print(test.test(np.ones(3)))
