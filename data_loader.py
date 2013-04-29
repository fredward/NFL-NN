import csv
import random
import itertools
'''
TODO:
	Optimize? Perhaps load the csv file into a dictionary (key: year, value: list of team data)
	for fast access each time its needed (i.e. not having to re-read through the whole csv file)
'''

class Data_Loader:
	def __init__(self):
		self.year_dict = {}
		# load the list of input vectors for a given year
		# year is in the 2nd column of the csv file
		datafile = open('playoffTeams.csv', 'rU')

		#skip first line
		datafile.readline()
		for row in datafile:
			data = row.strip().split(',')
			
			(team,year) = (data.pop(0),int(data.pop(0)))
			if year in self.year_dict:
				data = [int(float(x)) for x in data]
				output = [0, 0, 0, 0, 0, 0]
				classif = data.pop(0)
				output[classif] = 1
				self.year_dict[year].setdefault(classif,[]).append(((year,team),data))
			else:
				self.year_dict[year] = {}
				data = [int(float(x)) for x in data]
				output = [0, 0, 0, 0, 0, 0]
				classif = data.pop(0)
				output[classif] = 1
				self.year_dict[year].setdefault(classif,[]).append(((year,team),data))
		
			
			
	'''
	helper, converts classification number to output encoding 
	i.e. 1-5 to [0,0,0,0,0,1] etc.
	'''
	def encode(self, classification):
		o = [0,0,0,0,0,0]
		o[classification] = 1
		return o 


	'''
	returns an ordered tuple of inputs, targets for the given year
	'''				
	def getTargets(self,year):
		inputs = []
		targets = []
		for k,v in self.year_dict[year].items():
			inputs += zip(*v)[1]
			targets += itertools.repeat(self.encode(k),len(v))
		return inputs,targets
	
	'''
	Get all (data, stats) tuples for the given year
	'''	
	def getAllTeams(self,year):
		teams = []
		for v in self.year_dict[year].values():
			teams += v
		return teams
	



'''
Testing
'''		
if __name__ == "__main__":	
	dl = Data_Loader()
	print dl.getTargets(2000)
	print dl.getAllTeams(1992)
