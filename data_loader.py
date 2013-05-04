import csv
import random
import itertools
from team import Team
from random import choice, random
from math import pow, sqrt


'''
TODO:
    Optimize? Perhaps load the csv file into a dictionary (key: year, value: list of team data)
    for fast access each time its needed (i.e. not having to re-read through the whole csv file)
'''

class Data_Loader:

    data_list = [0,1,2,3,4,5,6,8,11,17,21,22,23,29,35,39]
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
            #print "Row :" + str(data) + "\n"
            #print "Year: " + str(year) + "\ndata[1] :" + str(data[1]) + "\n"
            
            #print "SAME!\n"
            (name,year) = (data.pop(0),int(data.pop(0)))
    
            #print (year,team)
            if year in self.year_dict:
                data = [float(x) for x in data]
                classif = int(data.pop(0))
                output = self.encode(classif)
                data = [data[i] for i in self.data_list]
                self.year_dict[year].setdefault(classif,[]).append(Team(name,year,data,classif))

            else:
                self.year_dict[year] = {}
                data = [float(x) for x in data]
                
                classif = int(data.pop(0))
                output = self.encode(classif)
                data = [data[i] for i in self.data_list]
                self.year_dict[year].setdefault(classif,[]).append(Team(name,year,data,classif))

            
            
            
    '''
    helper, converts classification number to output encoding 
    i.e. 1-5 to [0,0,0,0,0,1] etc.
    '''
    '''def encode(self, classification):
        o = [0,0,0,0,0,0]
        o[classification] = 1
        return o 
    '''
    def encode(self, classification):
        return [float(classification)/5]

    '''
    reverse encodes an output encoding to a classification number
    Parameters: 
        encoding: the encoding array
    Return:
        classification: an in representing the classification
    '''  
    '''
    def rev_encode(self, encoding):
        return encoding.index(1)
    '''
    def rev_encode(self, enc_classification):
        return enc_classification[0] * 5.0

    '''
    returns an ordered tuple of inputs, targets for the given year
    '''             
    def getTargets(self,years):
        inputs = []
        targets = []
        for year in years:
	        for k,v in self.year_dict[year].items():
	            inputs += reduce(lambda a, b : a + [b.stats],v, list())
	            targets += itertools.repeat(self.encode(k),len(v))
        return inputs,targets
    
    '''
    returns an 5 member ordered tuple of inputs, targets, with one from each class (randomly selected
        for classifications with more than one member)
    '''
    def getBalancedTargets(self,years):
        inputs = []
        targets = []
        for year in years:
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
    Get all the times in the dictionary, for every year
    '''
    def getEveryTeam(self):
    	teams = []
    	for year in self.year_dict.values():
    		teams += reduce(lambda a,b: a + b, year.values())
    	return teams

    '''
    Get the given team by team code and year
    parameters:
        team: the team code as a string
        year: the year as an int
    return:
        the team as team object
    '''
    def getTeam(self, team, year):
        return filter(lambda t: t.name == team,self.getAllTeams(year))[0]


'''
Testing
'''     
if __name__ == "__main__":  
    dl = Data_Loader()
    #print dl.getBalancedTargets(2000)
    #print dl.getAllTeams(1992)
    all_i, all_t =  dl.getSmoteTargets([2008, 2009,2010,2011])
    smote = zip(all_i, all_t)
    smote_test_dict = {}
    for i,t in smote:
        smote_test_dict.setdefault(dl.rev_encode(t),[]).append(i)
    for k,v in smote_test_dict.items():
        print str(dl.encode(k)) + ": " + str(len(v))
    rk,rv = choice(smote_test_dict.items())
    for t in rv:
    	print str(dl.encode(rk))	 + " -> " + str(t)

