#!/usr/bin/python

from node import Node

class Neural_Network:
	
	'''
	instantiates lists of nodes for a 1 hidden layer neural network
	'''
	def __init__(self):
		self.hidden_nodes = []
		self.output_nodes = []
	'''
	static constructor for a neural network with random weigts from -0.1 to 0.1
	'''
	@staticmethod
	def createWithRandomWeights(i_count, h_count, o_count):
		nn = Neural_Network()
		for i in range(h_count):
			nn.hidden_nodes.append( Node.initWithRandomWeights(i_count) )
		for i in range(o_count):
			nn.output_nodes.append( Node.initWithRandomWeights(h_count) )
		return nn
		
		
		
	'''
  feed the input values forward, and return the result
  note: a + [x] is list concatenation in python
	'''
	def feed_forward(self, input):
		hidden_values = reduce( lambda a,b: a + [b.calculate_value(input)], self.hidden_nodes, list() ) 
		output_values = reduce( lambda a,b: a + [b.calculate_value(hidden_values)], self.output_nodes, list() ) 
		return output_values
	
'''
TESTING
'''
nn = Neural_Network.createWithRandomWeights(3,20,6)		
print nn.feed_forward([1,2,3])
	
