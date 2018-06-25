# To visualise the results we could pick a reference network and measure the average fitness dependent on the number of steps/mutations away from that network.

# For example the network 0100110 might have 50% of its states converging on 101, there are 8 networks 1 step away which on average may have 20% of their states being fit.
# It is likely that the statistics will be different for different reference networks which may suggest a perspective to look at this 24 dimensional space.

# Store the average fitness for each number of steps (0 to 24), if there is a higher maximum then the reference is more appropriate.

import numpy as np
import matplotlib.pyplot as plt 
import pickle

results = pickle.load( open( "results.p", "rb" ) )

# We can sample the space randomly which saves reading the fitness of 2^24 networks for each reference network.
options = range(2**24) 
np.random.shuffle(options)

maxima = np.zeros((2,100)) #first row is reference network, second is its maxima

#try out 100 different reference perspectives, and find the ones with the highest and lowest maxima
for x in range(100):
	reference = options[x]
	ref = np.binary_repr(reference,24)
	stats = np.zeros((2,25))

	for n in options[:10000]:
		state = np.binary_repr(n,24)
		d = bin(int(ref,2)^int(state,2))[2:].count('1')

		#keep a running average
		stats[0,d] = (stats[0,d]*stats[1,d] + results[0,n])/(stats[1,d]+1)  
		stats[1,d] = stats[1,d] + 1

	maxima[0,x] = ref
	maxima[1,x] = np.max(stats[0,:])

bestref = maxima[0,np.argmax(maxima[1,:])]
worstref = maxima[0,np.argmin(maxima[1,:])]


print bestref
print worstref
