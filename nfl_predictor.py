'''
Here we will take a team's stats and run it through the trained neural network. 
This will output the projected playoff results, as well as teams from the past that
produced a similar output result.
'''
from neural_network import Neural_Network
from math import pow, sqrt

class NFL_Predictor:
    
    '''
    create a predictor class
    Parameters:
        network:    a Neural_Network object
    '''
    def __init__(self, network):
        self.nn = network
        
    '''
    returns expected playoff wins from trained neural network
    Parameters:
        team_stats: A Team object
    Return:
        feed-forward result of team's stats from neural network (float list)
    '''
    def runPrediction(self, team_stats):
        return self.nn.feed_forward(team_stats)
        
        
    '''
    returns the team that produces the closest prediction to the given team
    Parameters:
        all:        A list of Team objects representing all the teams that 
                    should be compared with
                    stats must be ordered as required for the neural network
        team:       A single Team object 
        num_teams:  number of similar teams to return
    Return:
        list of tuples containing num_teams of similar teams in the format
        (((year, team_name), stats), least squares difference)
    '''
    def compareWithPastTeams(self, all, team, num_teams):
        all_ff_results = []
        team.result = self.runPrediction(team.stats)
        map(lambda t: t.set_result(self.runPrediction(t.stats)), all)
        distances_to_team = map(lambda t: (t, self.compareVector(team.result, t.result)), all)
        sorted_distances = sorted(distances_to_team, key = lambda (t,d): d)
        similar_teams = []
        for i in range(num_teams):
            similar_teams.append(sorted_distances.pop(0))
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
        
'''
Testing
'''   
if __name__ == "__main__":
    from data_loader import Data_Loader 
    
    DL = Data_Loader()
    '''
    nn = Neural_Network.createWithRandomWeights(66,40,6)    
        
    # train! with learning rate proportional to # of teams in the situations
    inputs = []
    targets = []
    for y in range(2005,2007):
        i,t = DL.getTargets(y)
        inputs += i
        targets += t 
        #print targets
    nn = nn.train(10000,inputs,targets,1.5)
    nn.saveToFile("predictortest.txt")
    '''
    nn = Neural_Network.createFromFile("predictortest.txt")
    teams_2011 = DL.getAllTeams(2011)
    pats_2011 = filter(lambda t: t.name == "nwe", teams_2011)[0]
    all_other_teams = filter(lambda t: t.name != "nwe", teams_2011)
    predictor = NFL_Predictor(nn)
    similar = predictor.compareWithPastTeams(all_other_teams, pats_2011, 3)
    for t,d in similar:
        print t.name + " " + str(d) + "\n"
    
    
     
    
    
        
        
    
        
        
    