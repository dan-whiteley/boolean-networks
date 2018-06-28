from __future__ import division

# Now that we have found a good cluster of fit networks from the 24D space we can visualise this small area in more detail.

# There will be 24 networks 1 step away, 276 2 steps away, and 2024 3 steps away, so even with one pixel per network 3 steps away is stretching what can be visualised.

import numpy as np
import matplotlib.pyplot as plt 
import pickle

results = pickle.load( open( "results.p", "rb" ) )

# The reference network is

reference = '101111010000001000001100'

# the local network can be stored in a list, in decimal format so they index the results:

nearby = [[int(reference,2)],[],[]] #index = number of steps away

for i in range(24):

	mutation = 2**i
	one_away = mutation^int(reference,2)

	nearby[1].append(one_away)

	for j in range(24):

		if j!=i:
			mutation = 2**j
			two_away = mutation^one_away

			nearby[2].append(two_away)

#fitness can take on 9 values, 0-8, each of which should take a colour

colors = plt.cm.jet(np.linspace(0,1,9))


plt.figure()
for y in range(len(nearby)):
	for x in range(len(nearby[y])):
		result = int(results[0,nearby[y][x]])
		plt.plot((x+1)*len(nearby[2])/(len(nearby[y])+1),y,'.',color=colors[result])

# legend
for k in range(9):
	plt.plot(k*10,0,'o',color=colors[k])

plt.axis([-1,560,-0.2,2.2])
plt.show()

