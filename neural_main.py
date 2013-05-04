from neural_network import Neural_Network
from data_loader import Data_Loader
from itertools import izip, count 
from nfl_predictor import NFL_Predictor
import os
import argparse
'''
A main file, for directing user input from the highest level. Will load and use
all our other classes
'''

def train(args):
	#try:
		
		inputs = []
		targets = []
		y = range(args.start,args.end+1)
		if(args.db == 'u'):
			dl = Data_Loader()
			i,t = dl.getTargets(y)
		elif(args.db == 'b'):
			dl = Data_Loader()
			i,t = dl.getBalancedTargets(y)
		elif(args.db == 'p'):
			dl = Data_Loader('playoffTeams.csv')
			i,t = dl.getTargets(y)
		elif(args.db == 'o'):
			dl = Data_Loader('balancedData.csv')
			i,t = dl.getTargets(y)
		elif(args.db == 's'):
			dl = Data_Loader()
			print 'Creating SMOTE targets...'
			i,t = dl.getBLSmoteTargets(y,35)
			#i,t = dl.getSmoteTargets(y)
		inputs += i
		targets += t
		#create NN
		# if file already exists, build on that training
		if (os.path.exists(args.file)):
			print "file exists"
			nn = Neural_Network.createFromFile(args.file)
			pass
		else:
			print "file does not exist"
			nn = Neural_Network.createWithRandomWeights(len(inputs[0]),args.nodes,len(targets[0]))
		
		#train NN with the given data
		print 'Beginning Training...'
		nn = nn.train(args.epochs,inputs,targets,args.learn_rate)
		nn.saveToFile(args.file)
		print "Neural Network saved to %s" % (args.file)
	#except Exception as e:
		print "invalid formatting, consult neural_main.py t --help \n Error: %s" % e

def predict(args):
	try:
		nn = Neural_Network.createFromFile(args.file)
		dl = Data_Loader()

		#team = dl.getTeam(args.team, args.year)
		team = dl.getTeam(args.team, args.year)

		print "RESULTS: %s \n EXPECTED: %s" % (nn.feed_forward(team.stats), dl.encode(team.classification))
		post_processor = NFL_Predictor(nn)
		similar_teams = post_processor.compareWithPastTeams(dl.getEveryTeam(), team, 15)
		for t in similar_teams:
			print "%s \tScore: %f" % t
	except Exception as e:
		print "invalid formatting, consult neural_main.py t --help \n Error: %s" % e

def cross_validate(args):
	encode = Data_Loader().encode
	find_error = NFL_Predictor().compareVector
	try:	
		nn = Neural_Network.createFromFile(args.file)
		print "Loaded Neural Network with %i hidden nodes" % len(nn.hidden_nodes)
		totalCorrect = 0.0
		total_tested = 0.0
		for y in range(args.start,args.end+1):
			classRight = [0, 0, 0, 0, 0, 0]
			correct = incorrect = 0
			if(args.db == 'u'):
				dl = Data_Loader()
				teams = dl.getAllTeams(y)
			elif(args.db == 'b'):
				dl = Data_Loader()
				teams = dl.getAllTeams(y)
			elif(args.db == 'p'):
				dl = Data_Loader('playoffTeams.csv')
				teams = dl.getAllTeams(y)
			elif(args.db == 'o'):
				dl = Data_Loader('balancedData.csv')
				teams = dl.getAllTeams(y)
			print "testing %i teams from %i" % (len(teams),y)
			total_tested += len(teams)
			total_error = 0.0
			for t in teams:
				t.result = nn.feed_forward(t.stats)
				error = (find_error(t.result, encode(t.classification)))
				total_error += error**2
				if error < .1:
					correct += 1
					classRight
				if args.v:
					print "team %s, results %s, class %s, error %s" % (t.name, t.result, encode(t.classification), error)
				'''
				max_index = max(izip(t.result, count()))[1] 
				if (max_index == t.classification):
					#print "%s (%d) Correct" % (t.name, y)
					correct += 1
					classRight[t.classification] += 1
				else:
					#print "%s (%d) incorrect" % (t.name, y)
					incorrect += 1
				pass
				'''
			print "%d \t %d \t %s" % (y, correct, str(total_error))
			totalCorrect += correct
		print "totalCorrect: %d, %f" % (totalCorrect, totalCorrect/total_tested)
	except Exception as e:
		print "invalid formatting, consult neural_main.py c --help \nError: %s" % e


parser = argparse.ArgumentParser(description='Predict NFL playoff results with OR train a neural network on NFL results')

subparsers = parser.add_subparsers(help='Possible Actions')

'''
Create a parser for the train command, specified with 't'
'''
parser_train = subparsers.add_parser('t',help='train a NN over start-end years for e epochs')
parser_train.add_argument('nodes',type=int,help='number of hidden nodes')
parser_train.add_argument('db',type=str,help='data balancing method, u: unbalanced, o: oversampled, b:undersampled, p:playoffTeams, s: SMOTE',choices="uobps")
parser_train.add_argument('start',type=int,help='starting year to train on')
parser_train.add_argument('end',type=int,help='ending year')
parser_train.add_argument('epochs',type=int,help='number of epochs to train for')
parser_train.add_argument('learn_rate',type=float,help='the NN learning rate')
parser_train.add_argument('file',type=str,help='NN output file')
# set the function to be called when this parses is used
parser_train.set_defaults(func=train)

'''
Create a parser for the cross_validate command, specified with 'c'
'''
parser_cross = subparsers.add_parser('c',help='compare predicted outcomes with actual outcomes')
parser_cross.add_argument('start',type=int,help='starting year to train on')
parser_cross.add_argument('end',type=int,help='ending year')
parser_cross.add_argument('db',type=str,help='data balancing method, u: unbalanced, o: oversampled, b:undersampled, p:playoffTeams',choices="uobp")
parser_cross.add_argument('file',type=str,help='NN input file')
parser_cross.add_argument('-v',action='store_true')
# set the function to be called when this parses is used
parser_cross.set_defaults(func=cross_validate)

'''
Create a parser for the predict command, specified with 'p'
'''
parser_pred = subparsers.add_parser('p',help='predict the given team\'s based on the given NN')
parser_pred.add_argument('team',type=str,help='team to predict')
parser_pred.add_argument('year',type=int,help='year to predict')
parser_pred.add_argument('file',type=str,help='NN file to load')
# set the function to be called when this parser is used
parser_pred.set_defaults(func=predict)

args = parser.parse_args()
args.func(args)
