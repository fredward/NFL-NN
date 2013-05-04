'''
Will perform SMOTE oversampling to fix data imbalance problem in our data
Parameters:
	years:  a list of years that we should do SMOTE processing on
Return:
	a tuple of ordered lists representing the input stats and target results for ever
	team and SMOTE-produced synthetic team in the years provided
'''
def getSmoteTargets(self, teams):
	by_class = {}
	for t in teams:
		by_class.setDefault(t.classification, []).append(t)
	largest_classification = reduce(lambda m,l:  max(m, len(l)), all_years.values(), 0)
	#print "years: "+ all_years
	for l,c in all_years.items():
		oversample_amount = 3 #largest_classification/float(len(c))
		#print "amount: " + str(oversample_amount)
		#print len(c)
		if oversample_amount > 1:
		 #   print "in range for smote"
			for i in range(len(c)):
				t = c[i]
				number_of_neighbors = int(round(oversample_amount))
				neighbors = self.getClosestNeighbors(t, c, number_of_neighbors)
				new_data = map(lambda n: (self.vectorBetweenVectors(t.stats,n.stats), self.encode(t.classification)), neighbors)
				oversampled+=new_data
		else:
			#print "over threshold for smote: " +str(self.encode(c[0].classification))
			oversampled+= map(lambda t: (t.stats, self.encode(t.classification)), c)
	inputs, targets = zip(*oversampled)
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