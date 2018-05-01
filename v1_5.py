'''

Take 10,000 random networks and output their attractor states, so that we can visualise how nearby networks are similar or not.

Important final states are the ones arising from [1000010000] (anterior) and [0000000000] (posterior), as these are the initial states in Giacomantonio et al.

Desired Anterior State = [1,0,1,0,1,x,x,x,x,x] = 672 to 703, Posterior = [0,1,0,1,0,x,x,x,x,x] = 320 to 351

Also important to mark whether they are stable points (desirable), or cycles (probably not desirable).

'''
import numpy as np 
import matplotlib.pyplot as plt

def parents(child,graph,base):
	#find parents
	up = graph[child][0]
	#make sure no repeats
	for b in base:
		if b in up:
			up.remove(b)
	#add to visits
	for a in up:
		visits.append(a)
		#find parents of parents
		parents(a,graph,base)



fixed = np.zeros((10,10))
for i in range(5,10):	
	fixed[i,i-5]=1
for row in range(5):
	for column in range(5,10):
		if (row+column)%2==0:
			fixed[row,column] = -1
		else:
			fixed[row,column] = 1


#loop over many selections

network = range(2**24) 
np.random.shuffle(network)   #randomize the selection

samplesize = 10000
output = [['',[],[],[],[]] for x in range(samplesize)]        #[network, point attractors, cycle attractors, posterior result, anterior result]

for m in range(samplesize):
	n = network[m]
	b = np.binary_repr(n,24)      #keeps width fixed
	b = b[:4] + '1' + b[4:] 	  #adds the one for the constant Sp8 to Fgf8 interaction
	s = np.array(list(b)).reshape(5,5)

	output[m][0] = b

	selection = np.ones((10,10))
	selection[0:5,5:10] = s 

	#find the interaction matrix

	interaction = selection * fixed

	#split into AND and NOT matrices

	am = np.argwhere(interaction==1) 
	nm = np.argwhere(interaction==-1) 

	#FIND ALL STATES
	results = np.zeros((2**10,10))
	targets = []

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



		targets.append(results[i,9] + 2*results[i,8] + 4*results[i,7] + 8*results[i,6] + 16*results[i,5] + 32*results[i,4] + 64*results[i,3] + 128*results[i,2] + 256*results[i,1] + 512*results[i,0])



	#graph[n] gives the parent node and child nodes
	graph = [[[],[]] for x in range(1024)]

	targets = [int(z) for z in targets]

	for y in range(1024):
		graph[y][1] = targets[y]			#add child
		graph[targets[y]][0].append(y)		#add parent

	visits = []

	while len(visits)<1024:

		#find where to start
		for q in range(1024):
			if not (q in visits):
				break

		#find base nodes
		while not (q in visits):
			visits.append(q)
			q = graph[q][1]


		base = visits[visits.index(q):]

		#add parents to visits
		for each in base:
			parents(each,graph,base)

		if len(base)==1:
			output[m][1] = output[m][1] + base
		else:
			output[m][2] = output[m][2] + base

	#find main posterior result

	visits = []

	q = 0

	while not (q in visits):
		visits.append(q)
		q = graph[q][1]

	if len(visits[visits.index(q):])==1:
		output[m][3] = output[m][3] + visits[visits.index(q):]

	#find main anterior result

	visits = []

	q = 528			#1000010000

	while not (q in visits):
		visits.append(q)
		q = graph[q][1]

	if len(visits[visits.index(q):])==1:
		output[m][4] = output[m][4] + visits[visits.index(q):]

print(output)