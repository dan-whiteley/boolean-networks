# Search through the results for the best cluster. The space of networks is 24D, with each dimension having a value of 1 or 0.
# To get an estimate for how good a location is for a cluster do a weighted sum, adding the fitnesses weighted by 1/d*(24 choose d)

# start with '00000000000000000000' and try out all 24 mutations on it.
# calculate the score for each and keep the highest, do the same again but avoid mutating back to the original.
# repeat
# print out the best
#
# the graph of the 'landscape' is a slice of one path through the 24D network, each value on the x axis is a network and the y value is a measure of how fit its surrounding networks are.

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt 
import pickle

results = pickle.load( open( "results.p", "rb" ) )

# to save on computation later...
ncr = [] #N choose R, N = 24, R = index
num = 1
for i in range(25):
	ncr.append(num)
	num = num * (24-i) / (i+1)


state = '101111010000001000000000'

trials = 100000

landscape = []

options = range(2**24) 
np.random.shuffle(options)

avoid = []

for z in range(24):

	scores = bools = [['',0] for x in range(24)]
	
	for n in range(24):
		if not (n in avoid):
			mutation = np.binary_repr(2**n,24)
			new = bin(int(mutation,2)^int(state,2))[2:]

			#find the score

			score = 0

			for x in options[:trials]:
				#using the network as an option to mutate the new network, as this means you only have to randomise the 2**24 once.
				mut = np.binary_repr(x,24)
				sample = bin(int(new,2)^int(mut,2))[2:]
				d = mut.count('1')
				score = score + results[0,int(sample,2)]/d/ncr[d]

			scores[n][0] = new
			scores[n][1] = score

	highest = max(scores, key=lambda x: x[1])
	landscape.append(highest)

	#make the best network your new base state and repeat
	state = highest[0]
	avoid.append(scores.index(highest))

print landscape

t = range(24)
y = []
for i in t:
	y.append(landscape[i][1])

plt.plot(t,y)
plt.show()

## best result 111111010000001010111100