#!/usr/bin/python
from math import exp
class Node:
	#the list of weights to be applied to the input
	weights = []
	calculated_value = 0
	
	def __init___(self, ws):
		if ws == None:
			self.weights = []
		else:
			self.weights = ws
			
	# the sigmoid		
	def sigmoid (self, x):
		return 1/(1+exp(-x))
	
	def calculate_value (self, input):
		def weight_sum (a,b):
			#take the first item off and put it on the back
			w = weights.pop()
			weights.append(w)
			#sum with that weight * the corresponding input vector
			return a + w*b
				
		cv = reduce(weight_sum, input, 0)
		calculated_value = sigmoid(cv)
		return calculated_value
		