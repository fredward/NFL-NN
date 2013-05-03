from node import Node
from itertools import cycle
from data_loader import Data_Loader
import cPickle as pickle

'''
A class that defines a one hidden layer Neural Network
'''
class Neural_Network:
	
	'''
	instantiates lists of nodes for a 1 hidden layer neural network
	'''
	def __init__(self):
		self.hidden_nodes = []
		self.output_nodes = []
		
		
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
	def back_prop(self, input, t, learning_rate):
		 
		# copy t so we can pop and not destroy our data
		target = t[:] 
		#get the feed_forward output for the given input
		output = self.feed_forward(input)
		
		#pop through the error and use it to set the deltas for each output node
		map( lambda n: (n.set_delta((target.pop(0) - output.pop(0)) * (n.calculated_value*(1-n.calculated_value)))), self.output_nodes)	 
		
		'''
		the hidden nodes are a tad more complicated, as they require summation from the deltas of each downstream nodes, to get the
		weighted error for each hidden node
		'''
		e_values = []
		for i in range(len(self.hidden_nodes)):
			e_values.append( reduce( lambda a, b: a + (b.delta * b.weights[i]), self.output_nodes, 0))
			
		'''
		use each corresponding weighted error, to set the delta for each hidden node
		'''
		map( lambda n: (n.set_delta(e_values.pop(0) * (n.calculated_value*(1-n.calculated_value)))),self.hidden_nodes)
			
		# the new neural network to be returned
		new_nn = Neural_Network()
		
		#helper cycles for the map functions (   no mapi in python :-(   )
		h_cyc = cycle(self.hidden_nodes)
		i_cyc = cycle(input)		
		'''
		for each output node, calculate the new weights, and add a new node with those weights to a new neural network. 
		The cycles are needed because we must access the 'upstream' nodes and get their calculated values
		'''
		for o in self.output_nodes:
			new_nn.output_nodes.append(Node( map( lambda w: w + ((h_cyc.next().calculated_value)*(o.delta)*(learning_rate)), o.weights)))
			
		'''
		do the same fot the hidden nodes
		'''
		for h in self.hidden_nodes:
			new_nn.hidden_nodes.append(Node( map( lambda w: w + ((i_cyc.next())*(h.delta)*(learning_rate)), h.weights)))
		
			
		return new_nn
	
	'''
	Train on set of inputs and targets, for given # of epochs, with the given learning rate
	'''
	def train(self, epochs, inputs, targets, learning_rate):
			for e in range(epochs):
				print "epoch: %i" % (e+1)
				for i,t in zip(inputs, targets):
					#print "%f, %s" % (learning_rate(t), t)
						
					self = self.back_prop(i,t, learning_rate)
					
			return self

	'''
	Using Python's built in pickle module, we can save the neural network as an object in a file
	'''
	def saveToFile (nn, filename):
		file = open (filename, 'w')
		pickle.dump(nn, file)
		file.close()

	'''
	Also using pickle, we can use the saved neural network
	'''
	@staticmethod
	def createFromFile (filename):
		file = open (filename, 'r')
		nn = pickle.load (file)
		return nn	
	
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
				

