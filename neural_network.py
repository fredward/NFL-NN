#!/usr/bin/python

from node import Node
from itertools import cycle
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
		hidden_values = reduce( lambda a,b: a + [b.calculate_value(input)], self.hidden_nodes, [] ) 
		output_values = reduce( lambda a,b: a + [b.calculate_value(hidden_values)], self.output_nodes, [] ) 
		return output_values
	'''
	the back propagation algorithm
	takes a output and a target and updates the weights via gradient descent
	'''
	def back_prop(self, input, target, learning_rate):
		#pop through the error and use it to set the deltas for each output node
		output = self.feed_forward(input)
		map( lambda n: (n.set_delta((target.pop(0) - output.pop(0)) * (n.calculated_value*(1-n.calculated_value)))), self.output_nodes)	 
		
		'''
		for i in range(len(self.output_nodes)):
			self.output_nodes[i].set_delta((target[i] - output[i]) * (self.output_nodes[i].calculated_value*(1-self.output_nodes[i].calculated_value)))
		'''
		'''
		the hidden nodes are a tad more complicated, as they require summation from the deltas of each downstream nodes
		'''
		e_values = []
		for i in range(len(self.hidden_nodes)):
			e_values.append( reduce( lambda a, b: a + (b.delta * b.weights[i]), self.output_nodes, 0))
		map( lambda n: (n.set_delta(e_values.pop(0) * (n.calculated_value*(1-n.calculated_value)))),self.hidden_nodes)
		'''
		for i in range(len(self.hidden_nodes)):
			e = 0
			for o in range(len(self.output_nodes)):
				e += self.output_nodes[o].delta * self.output_nodes[o].weights[i]
			e_values.append(e)
		# create the new neural network
		for i in range(len(self.hidden_nodes)):
			self.hidden_nodes[i].set_delta(e_values[i] * (self.hidden_nodes[i].calculated_value * (1-self.hidden_nodes[i].calculated_value)))
		'''
			
		new_nn = Neural_Network()
		
		#helper cycles for the map functions (   no mapi in python :-(   )
		h_cyc = cycle(self.hidden_nodes)
		i_cyc = cycle(input)
		
		for o in self.output_nodes:
			'''	
			new_w = []
			for i in range(len(o.weights)):
				new_w.append( o.weights[i] + ((h_cyc.next().calculated_value)*(o.delta)*(learning_rate)) )
			new_nn.output_nodes.append( Node( new_w ) )
			'''
			new_nn.output_nodes.append(Node( map( lambda w: w + ((h_cyc.next().calculated_value)*(o.delta)*(learning_rate)), o.weights)))
			
		for h in self.hidden_nodes:
			'''
			new_w = []
			for i in range(len(h.weights)):
				new_w.append( h.weights[i] + (i_cyc.next())*(h.delta)*(learning_rate)) 
			new_nn.hidden_nodes.append( Node( new_w ) )
			'''
			new_nn.hidden_nodes.append(Node( map( lambda w: w + ((i_cyc.next())*(h.delta)*(learning_rate)), h.weights)))
			
		return new_nn
		
'''
TESTING
'''
nn = Neural_Network.createWithRandomWeights(3,15,1)		
#attempting to learn 'true' for an input with one zero.
for i in range(50000):
	#nn=nn.back_prop([1,1,1], [1,1], .5)
	nn=nn.back_prop([1,1,0], [1,0], .5)
	nn=nn.back_prop([1,0,1], [0,1], .5)
	nn=nn.back_prop([0,1,1], [0,1], .5)
	nn=nn.back_prop([1,0,0], [0,0], .5)
	nn=nn.back_prop([0,0,1], [0,1], .5)
	nn=nn.back_prop([0,1,0], [0,0], .5)
	#nn=nn.back_prop([0,0,0], [0,0], .5)
	if i % 10000 == 0:
		print "epoch: " + str(i) + " complete!"
res = nn.feed_forward([1,1,1])
print "End \tout: " + str(res) 	
res = nn.feed_forward([0,0,0])
print "End \tout: " + str(res)+ "\n"

	
