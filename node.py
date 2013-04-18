#!/usr/bin/python
from math import exp
from random import randint
class Node:
	#the list of weights to be applied to the input
	
	def __init__(self, ws):
		if ws == None:
			self.weights = []
		else:
			self.weights = ws
		self.calculated_value = 0
		self.delta = 0
	
	'''
	static constructor for a node with random weights from -0.1 to 0.1
	'''
	@staticmethod		
	def initWithRandomWeights(length):
		ws = []
		for i in range(length):
			ws.append( (randint(0,20)-10) / 10 )
		return Node(ws)
		
	# the sigmoid	'rounds' if numbers are egregious
	def sigmoid (self, x):
		
		if x > 100:
			return 1
		elif x < -100:
			return 0
		
		return 1.0/(1.0+exp(-x))
	
	'''
	calculate the activation value of the node given the input vector (and store it)
	'''
	def calculate_value (self, input):
		if len(input) == len(self.weights):
			'''
			def weight_sum (a,b):
				#take the first item off and put it on the back
				w = self.weights.pop(0)
				self.weights.append(w)
				#sum with that weight * the corresponding input vector
				return a + b*w
			cv = reduce(weight_sum, input, 0)
			'''
			cv = 0
			for i in range(len(self.weights)):
				cv += input[i]*self.weights[i]
			
			#store the calculated value in the node instance
			self.calculated_value = self.sigmoid(cv)
			
			return self.calculated_value
		else:
			raise Exception("Wrong number of inputs")
	
	def set_delta(self, d):
		self.delta = d	
	
	def inc_delta(self, d):
		self.delta += d
'''
TESTING
'''
n = Node([-.2,-.1,0,.1,.2,.234,1.3])
test_inputs = [10,20,4,10,2,3,1]

