'''
Class that defines a team
With a name, year, 66 member stats array and possible feed-forward result
'''


class Team:
	def __init__(self, n, y, s, c):
		self.name = n
		self.year = y
		self.stats = s
		self.classification = c
		self.result = []
	
	'''
	accessor method for results, useful because lambdas cannot contain assignments
	'''	
	def set_result(self, r):
		self.result = r