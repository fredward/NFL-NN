from neural_network import Neural_Network
from data_loader import Data_Loader
'''
A main file, for directing user input from the highest level. Will load and use
all our other classes
'''

'''
PLAN:

Do we want to Train or Predict

If Train:
	Pick/Choose the training / testing test -> go train on X interations
	
If Predict:
	1) Choose the NN file (weights) you want to load, and present a way to input team data
		a) scrape from website OR just copy/paste into terminal
	2) Run through the NN
	3) Present output
		a) predicted playoff finish
		b) which teams is this team 'most like'
		c) hopefully some graphics and stuff
		
This can all be done just in a straight forward imperative script

'''

import argparse


def train(args):
	print 'train'
	nn = Neural_Network.createWithRandomWeights(66,args.nodes,6)
	dl = Data_Loader()
	inputs = []
	targets = []
	for y in range(args.start,args.end):
		i,t = dl.getTargets(y)
		inputs += i
		targets += t
	nn = nn.train(args.epochs,inputs,targets,args.learn_rate)
	nn.saveToFile(args.file)

def predict(args):
	nn = Neural_Network.createFromFile(args.file)
	dl = Data_Loader()
	team = dl.getTeam(args.team, args.year)
	print nn.feed_forward(team.stats)



parser = argparse.ArgumentParser(description='Predict NFL playoff results with OR train a neural network on NFL results')

subparsers = parser.add_subparsers(help='Possible Actions')
parser_train = subparsers.add_parser('t',help='train a NN over start-end years for e epochs')
parser_train.add_argument('nodes',type=int,help='number of hidden nodes')
parser_train.add_argument('start',type=int,help='starting year to train on')
parser_train.add_argument('end',type=int,help='ending year')
parser_train.add_argument('epochs',type=int,help='number of epochs to train for')
parser_train.add_argument("learn_rate",type=float,help='the NN learning rate')
parser_train.add_argument('file',type=str,help='NN output file')
parser_train.set_defaults(func=train)

parser_pred = subparsers.add_parser('p',help='predict the given team\'s based on the given NN')
parser_pred.add_argument('team',type=str,help='team to predict')
parser_pred.add_argument('year',type=int,help='year to predict')
parser_pred.add_argument('file',type=str,help='NN to load')
parser_pred.set_defaults(func=predict)

args = parser.parse_args()
args.func(args)
