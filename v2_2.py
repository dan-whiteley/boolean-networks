# Plot Average Fitness as a function of the number of mutational steps away from the reference network.

import numpy as np
import matplotlib.pyplot as plt 
import pickle

results = pickle.load( open( "results.p", "rb" ) )

options = range(2**24) 
np.random.shuffle(options)

plt.figure()
x = np.arange(25)

#A close to fit network

ref1 = '111111010000001010111100'
stats = np.zeros((2,25))
for n in options[:1000000]:
	state = np.binary_repr(n,24)
	d = bin(int(ref1,2)^int(state,2))[2:].count('1')

	#keep a running average
	stats[0,d] = (stats[0,d]*stats[1,d] + results[0,n])/(stats[1,d]+1)  
	stats[1,d] = stats[1,d] + 1

plt.plot(x,stats[0,:])

#A far from fit network

ref2 = '101101110100000000000000'
stats = np.zeros((2,25))
for n in options[:1000000]:
	state = np.binary_repr(n,24)
	d = bin(int(ref2,2)^int(state,2))[2:].count('1')

	stats[0,d] = (stats[0,d]*stats[1,d] + results[0,n])/(stats[1,d]+1)  
	stats[1,d] = stats[1,d] + 1

plt.plot(x,stats[0,:])

plt.show()	