# Random boolean nets with 3 genes, so 2^(3*2^3) possible networks

# In this first attempt fitness is measured by the number of states which converge on a point attractor '101', so could be any integer 0-8.

# See intro.txt for information about how the networks and states are coded as binary strings.
# In essence each network can be represented by a 24 bit string, where each bit is the outcome of one row of the truth table, 8 rows for each gene.

import numpy as np 
import matplotlib.pyplot as plt 

results = np.zeros((1,2**24))

#cycle through each network
for x in range(2**24):
	out = np.binary_repr(x,24)
	#only 1 in 8 of them will have the stable point at all...
	if (out[5] == '1' and out[13] == '0' and out[21] == '1'):
		
		#find parent nodes of state 101
		children = ['101']
		parents = []

		while children:
			for child in children:
				for y in range(8):
					state = np.binary_repr(y,3)
					if state == child:
						break
					else:
						output = out[y]+out[y+8]+out[y+16]
						if output == child:
							children.append(state)

				parents.append(child)
				children.remove(child)

		results[0,x] = len(parents)


#save the results in python friendly format
import pickle

pickle.dump(results , open("results.p","wb"))

