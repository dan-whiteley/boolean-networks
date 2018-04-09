'''

Take 1 successful network at random and look at the state space dynamics for it.

Desired Anterior State = [1,0,1,0,1,x,x,x,x,x] = 672 to 703, Posterior = [0,1,0,1,0,x,x,x,x,x] = 320 to 351

'''
import numpy as np 
import matplotlib.pyplot as plt

#initialise fixed matrix
'''
00000+-+-+
00000-+-+-
00000+-+-+
00000-+-+-
00000+-+-+
+000000000
0+00000000
00+0000000
000+000000
0000+00000
'''

fixed = np.zeros((10,10))
for i in range(5,10):
	fixed[i,i-5]=1
for row in range(5):
	for column in range(5,10):
		if (row+column)%2==0:
			fixed[row,column] = -1
		else:
			fixed[row,column] = 1


#loop over every selection
#will break when it finds the first success

successes = []

n = 4270766				  #random successful network
b = np.binary_repr(n,24)      #keeps width fixed
b = b[:4] + '1' + b[4:] 	  #adds the one for the constant Sp8 to Fgf8 interaction
s = np.array(list(b)).reshape(5,5)

selection = np.ones((10,10))
selection[0:5,5:10] = s 

#find the interaction matrix
interaction = selection * fixed

#split into AND and NOT matrices

am = np.argwhere(interaction==1) 
nm = np.argwhere(interaction==-1) 


#loop through all possible states (2**10), and find where they evolve to

results = np.zeros((2**10,10))
graph = []

for i in range(2**10):
	binary = np.binary_repr(i,10)
	state = np.array(list(binary))
	state = [int(z) for z in state]


	#generate lists of effecting bools for each variable
	bools = [[] for x in range(10)]

	for [x,y] in am:
		bools[x].append(state[y])
	for [x,y] in nm:
		bools[x].append(1-state[y])

	#the state at the next time step is the product of each list in bools
	for j in range(10):
		results[i,j] = np.prod(bools[j])



	graph.append(results[i,9] + 2*results[i,8] + 4*results[i,7] + 8*results[i,6] + 16*results[i,5] + 32*results[i,4] + 64*results[i,3] + 128*results[i,2] + 256*results[i,1] + 512*results[i,0])


print graph