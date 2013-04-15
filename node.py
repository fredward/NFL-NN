#!/usr/bin/python
from math import exp
class Node:
	#the list of weights to be applied to the input
	weights = []
	calculated_value = 0
	
	def __init__(self, ws):
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
			w = self.weights.pop(0)
			
			self.weights.append(w)
			#sum with that weight * the corresponding input vector
		
			return a + b*w
				
		cv = reduce(weight_sum, input, 0)
		
		self.calculated_value = self.sigmoid(cv)

		return self.calculated_value
		


