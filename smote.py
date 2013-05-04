from math import ceil
from random import sample

class SmoteTools:

	def __init__(self):
		'''
		number of neighbors to look at when judging the borderline of a classification
		'''
		self.neighbor_num = 10
		
	'''
	returns a tuple of lists of stats, encoded targets for a specific classification
	Parameters:
		all_teams: all teams in the data set, as Team objects
		classificaton: the classification to do SMOTE processing on
		num: number of 
	'''
	def performBorderLineSmote(self, all_teams, classification, num):
		bl_teams = self.getBorderLineTeams(all_teams, classification)
		return getSyntheticTargets(bl_teams, num)
		
			
	'''
	find teams on the "borderline" of a given classification
	Parameters:
		all_teams: 		all teams in the dataset
		classification:	the classification category whose borderline should be found
	Return:
		a list of teams on the borderline of the given classification
	'''
	def getBorderLineTeams(self, all_teams, classification):
		bl_teams = []
		class_teams = filter(lambda t: t.classification = classification, all_teams)
		for ct in class_teams:
			ct_neighbors = self.getClosestNeighbors(ct, all_teams, self.neighbor_num)
			neighbors_in_class = len(filter(lambda t:t.classification == ct.classification, ct_neighbors))
			neighbors_out_of_class = len(filter(lambda t: t.classification != ct.classification, ct_neighbors))
			if neighbors_in_class > 0 and neighbors_out_of_class > neighbors_in_class:
				bl_teams.append(ct)
		return bl_teams
			
	
	'''
	Creates num SMOTE synthetic data points between each team and its neighbors in the list provided
	Parameters:
		teams:  a list of teams to create synthetic data from
		num: number of total synthetic teams to create
	Return:
		a tuple of ordered lists representing the input stats and target results of SMOTE synthetic
		data created from the given teams
	'''
	def getSyntheticTargets(self, teams, num):
		new_data = []
		total_teams = len(teams)
		amount_per_team = ceil(num/total_teams)
		for t in teams:
			neighbors = self.getClosestNeighbors(t, teams, amount_per_team)
			new_data = map(lambda n: (self.vectorBetweenVectors(t.stats, n.stats), self.encode(t.classification)), neighbors)
		
		inputs, targets = zip(*(random.sample(new_data,num)))
		return inputs, targets	    
	
	
	
	
	'''
	Returns a random vector on the segment between two vectors
	Parameters:
		v1,v2:  two vectors
	Return:
		the new vector
	'''
	def vectorBetweenVectors(self, v1, v2):
		new = []
		for i1,i2 in zip(v1,v2):
			new.append(i1+((i2-i1)*(random())))
		#print "old1: " +str(v1)
		#print "old2: " +str(v2)
		#print "new:  " + str(new)
		return new
	
	
	
	'''
	Gets the closest neighbors by euclidean distance
	Parameters
		t:          a Team object
		neighbors:  a list of Teams from which to select the closest neighbor
		num:        number of neighbors to select
	Return:
		a list of the num closest neighbors as Team objects
	'''
	def getClosestNeighbors(self, t, neighbors, num):
		# we need at least as many teams as there are closest neighbors required
		#distances_to_team = map(lambda m: (t, self.compareVector(t.stats, m.stats)), neighbors)
		sorted_distances = sorted(neighbors, key = lambda m: self.compareVector(t.stats, m.stats))
		similar_teams = []
		#fill up the list at the end with duplicates if we dont have enough
		while len(sorted_distances) < num:
			sorted_distances.append(choice(neighbors))
		for i in range(num):
			similar_teams.append(sorted_distances.pop(0))
		#print "simteam l " +str(len(similar_teams))
		return similar_teams
		
	'''
	compare two vectors by euclidean distance
	Parameters:
		v1,v2:  two lists of numbers representing a vector - assumes they are the same
				length because the neural network produces an output list of uniform
				length
	Return:
		euclidean distance between two vectors (float)
	'''
	def compareVector(self, v1, v2):
		sum = 0
		for i1,i2 in zip(v1,v2):
			sum += pow((i1-i2),2)
		return sqrt(sum)  