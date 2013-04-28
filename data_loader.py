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
		# year is in the 2nd column of the csv file'''	
		datafile = open('scaledData.csv', 'rU')
		
		#skip first line
		datafile.readline()
		for row in datafile:
			data = row.strip().split(',')
			#print "Row :" + str(data) + "\n"
			#print "Year: " + str(year) + "\ndata[1] :" + str(data[1]) + "\n"
			
			#print "SAME!\n"
			(team,year) = (data.pop(0),int(data.pop(0)))
			#print (year,team)
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
			
	
	

	@staticmethod
	def createFromRandomYear():
		year = random.randrange(1970, 2012)
		DL = Data_Loader(year)
				
		return DL
		
	@staticmethod
	def createFromYear(year):
		
		DL = Data_Loader(year)
				
		return DL
		
dl = Data_Loader()
print dl.getTargets(2000)
