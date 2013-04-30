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
    Will perform SMOTE oversampling to fix data imbalance problem in our data
    Parameters:
        years:  a list of years that we should do SMOTE processing on
    Return:
        a tuple of ordered lists representing the input stats and target results for ever
        team and SMOTE-produced synthetic team in the years provided
    '''
    def getSmoteTargets(self, years):
        all_years = [[] for x in range(6)]
        oversampled = []
        #for all the year range, make a list of lists by classifications - lists are tuple (input, target)
        for y in years:
            for (c,ts) in self.year_dict[y].items():
                map(lambda t: all_years[c].append(t), ts)
           # map(lambda (c,l): all_years[c].append((l, self.encode(c))), zip(self.year_dict[y].keys(), self.year_dict[y].values()))
            #print str(all_years)
        largest_classification = reduce(lambda m,l:  max(m, len(l)), all_years, 0)
        for c in all_years:
            oversample_amount = largest_classification/len(c)
            print len(c)
            if oversample_amount > 1:
                for i in range(len(c)):
                    t = c[i]
                    number_of_neighbors = int(round(oversample_amount-1))
                    neighbors = self.getClosestNeighbors(t, c, number_of_neighbors)
                    new_data = map(lambda n: (self.vectorBetweenVectors(t.stats,n.stats,random()), self.encode(t.classification)), neighbors)
                    oversampled+=new_data
        	else:
        		oversampled+= map(lambda t: (t.stats, self.encode(t.classification)), c)
        inputs, targets = zip(*oversampled)
        return inputs, targets
                    
                
                    

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
    return:
        the team as team object
    '''
    def getTeam(self, team, year):
        return filter(lambda t: t.name == team,self.getAllTeams(year))[0]


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
        if len(neighbors) < num:
            for i in range(num-len(neighbors)):
                neighbors.append(neighbors[0])
        distances_to_team = map(lambda m: (t, self.compareVector(t.stats, m.stats)), neighbors)
        sorted_distances = sorted(distances_to_team, key = lambda (t,d): d)
        similar_teams = []
        for i in range(num):
            similar_teams.append(sorted_distances.pop(0)[0])
        #print "simteam l " +str(len(similar_teams))
        return similar_teams
    
    '''
    Returns a vector on the segment between two vectors
    Parameters:
        v1,v2:  two vectors
        d:      distance between the two vectors where the new vector should be (0-1)
    Return:
        the new vector
    '''
    def vectorBetweenVectors(self, v1, v2, d):
        new = []
        for i1,i2 in zip(v1,v2):
            new.append(i1+((i1-i2)*d))
        return new
    
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

'''
Testing
'''     
if __name__ == "__main__":  
    dl = Data_Loader()
    #print dl.getBalancedTargets(2000)
    #print dl.getAllTeams(1992)
    
    print dl.getSmoteTargets([2000])
