import csv
import random
import itertools
from team import Team
from random import choice
'''
TODO:
	Optimize? Perhaps load the csv file into a dictionary (key: year, value: list of team data)
	for fast access each time its needed (i.e. not having to re-read through the whole csv file)
'''

class Data_Loader:

	def __init__(self,f=None):
		self.year_dict = {}
		# load the list of input vectors for a given year
		# year is in the 2nd column of the csv file'''
		if f == None:	
			datafile = open('scaledData.csv', 'rU')
		else:
			datafile = open(f, 'rU')
		#datareader = csv.reader(datafile, dialect=csv.excel_tab)

		#skip first line
		datafile.readline()
		for row in datafile:
			data = row.strip().split(',')

			#print "SAME!\n"
			(name,year) = (data.pop(0),int(data.pop(0)))
	
			#print (year,team)
			if year in self.year_dict:
				data = [float(x) for x in data]
				output = [0, 0, 0, 0, 0, 0]
				classif = int(data.pop(0))
				output[classif] = 1
				self.year_dict[year].setdefault(classif,[]).append(Team(name,year,data,classif))

			else:
				self.year_dict[year] = {}
				data = [float(x) for x in data]
				output = [0, 0, 0, 0, 0, 0]
				classif = int(data.pop(0))
				output[classif] = 1
				self.year_dict[year].setdefault(classif,[]).append(Team(name,year,data,classif))

			
			
			
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
			inputs += reduce(lambda a, b : a + [b.stats],v, list())
			targets += itertools.repeat(self.encode(k),len(v))
		return inputs,targets
	
	'''
	returns an 5 member ordered tuple of inputs, targets, with one from each class (randomly selected
		for classifications with more than one member)
	'''
	def getBalancedTargets(self,year):
		inputs = []
		targets = []
		for k,v in self.year_dict[year].items():
			# notice we are appending here because these are just single lists, not lists of lists
			inputs.append(choice(v).stats)
			targets.append(self.encode(k))
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
	Get the given team by team code and year
		parameters:
			team: the team code as a string
			year: the year as an int
		return value:
			the team as team object
	'''
	def getTeam(self, team, year):
		return filter(lambda t: t.name == team,self.getAllTeams(year))[0]


	'''
	Will perform SMOTE oversampling to fix data imbalance problem in our data
	'''
	def getSmoteTargets(team_dict):
		return None



'''
Testing
'''		
if __name__ == "__main__":	
	dl = Data_Loader()
	print dl.getBalancedTargets(2000)
	#print dl.getAllTeams(1992)
