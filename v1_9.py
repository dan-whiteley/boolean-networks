'''

Take 400 successful networks and output their attractor states, so that we can visualise how nearby networks are similar or not.

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


#initialise fixed matrix
fixed = np.zeros((10,10))
for i in range(5,10):
	fixed[i,i-5]=1
for row in range(5):
	for column in range(5,10):
		if (row+column)%2==0:
			fixed[row,column] = -1
		else:
			fixed[row,column] = 1

data = ['0001110110110101000101010','0110110011010101010000100','0001100111110101010000010','0001110110110001010001000','0001100100100101110000010','0101110010010101010001000','0101110111110001010000010','0011110001000010100001010','0101110001010100100001010','0100110001110100100001010','0101110011010101010101110','0101110101110001110001010','0010110110010011000101010','0100110100100100110001010','0101110001110101010001010','0011110100010101100100110','0101110101010101100001110','0100110100100000010101000','0101110100100111100000010','0001110100110001010001010','0101110110110101010101010','0100100011010001000100110','0010110001010111100001010','0001100011110101010000010','0101110100100101110001010','0100100110000111000001000','0101110100110101010000010','0001110001010001010100110','0011110110000111000101010','0011100011010101010000100','0011100010010101010001010','0100110100010100100100110','0101110011110001010001010','0101110100010100100000110','0101110001000100100001010','0111100010010101010001100','0101110100110101010001000','0101110001110001100001010','0010100011010001000100110','0101100010110111000101010','0111100010010101010101110','0001110010110011010101010','0001100001110001010000010','0101110111100001010001010','0101110011110001010000010','0100110100100100110101010','0001100110100001010001010','0001110100110100100000010','0110110101010111100001010','0100110100110001100000010','0100110010010101010101110','0100110100100000010001000','0001110010110111010101010','0101110100110001100001000','0101100110100101010000010','0101110100100100110101010','0111110001010010110001010','0111110010010111000101010','0101110010110011010001000','0100110101000101000101100','0101110100100000100101000','0101110101100001010001010','0001110101100001010000010','0101110001010101100001010','0101100110010111000101010','0101110010100101010101010','0001100010110001000101010','0001110010110101010101010','0101110010010101010101110','0100110001010100110000100','0101100110110101000101010','0101110100110001000101010','0010100011010101010001110','0110110110000111000101010','0001110010100001010000010','0110110110010111010101010','0101110101100011110001010','0101100010110101000101010','0001110001100001010000010','0010110001000110100001010','0110110101010011110001010','0011110010010101010001000','0001110100100101000101010','0011110010010101010101010','0101110001000011100001010','0111110101010100100101110','0001110100110001010101000','0101100011010101010101110','0001100010110011000101010','0100110001110001010000010','0010110001010011100001010','0011110101010111100001010','0100110100100000110101000','0100110101100110110001010','0100110100100100000101000','0001100010100101010101010','0100110001110000100001010','0110110010010111010101010','0100110100100000100101000','0001110110000011000101010','0100110100100101110101000','0101100010010001000101010','0100110001100110110001010','0101110011100101010001010','0101110001100101010000010','0111110101010111100001010','0011110001000110110001010','0100110001000011110001010','0010100010010101010100110','0001110011010101010000110','0101100010110101010001000','0010110110010111000101010','0101100010100111010101010','0001100110010111000101010','0101110110100011010101010','0100110110110000010001000','0101110110110101010001010','0100110101110011110001010','0100110101100100110001010','0011110001000101100101100','0100110100100101000101010','0101110110100001010001010','0100110100100101100000010','0001100110100111010101010','0001110010000111010101010','0111110011010101010101110','0101110001110110100001010','0100110101010101000101100','0000110100100100100001010','0100110011010101010001100','0100100011110101010001010','0101100010110001010001010','0001110110100101000101010','0110110001000101100001010','0001110100010010110000010','0001100110100011010101010','0110110001000111110001010','0001100010110001010000010','0101110101100111110001010','0100110001100111100001010','0101100110100101010101010','0101110001010010110001010','0101110100110101110001010','0100110001100011100001010','0100110101010111100001010','0001110100010100100001110','0001110011100101010001010','0000110010010101010000110','0100110100010101100001000','0101110001010110110001010','0100110100100000110101010','0101110100100001010101000','0100110100100101010001010','0100110101110001010001010','0001110000010101010000010','0001100010100001010000010','0001100110110001000101010','0011100010010101010001000','0101110101110110110001010','0001100110110011000101010','0101110001010101010100110','0100110101100011100001010','0101110110100101010001000','0101110001000011110001010','0110100010000011000101010','0111110010000111000101010','0111100010000101000101010','0001110000100101010000010','0000100110110000010001000','0100100011010101010000100','0100110101010101100001100','0101110101110111110001010','0101100010100101010001000','0100110101010110110001010','0011100010010001000101010','0001110100010100100000110','0110110010010011000101010','0100110001010100110000110','0101110101100100100001010','0010110101010101100001110','0101110100100000100101010','0001100010010111010101010','0101100010100001010001000','0111110001010011110001010','0000110010010101010100110','0100110001110111100001010','0100110100110000110101000','0010100011010001000001100','0101110100100100100000010','0100110100000101000001000','0111110100010101100001100','0110110101010101100001010','0100100101110001010000010','0100110100100001100001000','0100110101100000110001010','0001110000100001010000010','0011110010000011000101010','0100110001000111110001010','0111110100010100100100110','0111100010010111000101010','0111100011010101010001110','0101110011110101010000010','0011110110010111010101010','0001110100110100100001010','0101110101010011100001010','0100110100110001110101010','0100100110000111010001000','0010110001000011100001010','0000100111100101010001010','0001110100100101010001000','0100110001010101110000110','0111110100010101100101100','0101110100100001110000010','0000110100110100100101010','0101110010010111010101010','0101100011110001010001010','0010110101010101100001100','0001110011010101010101110','0101110110100111010101010','0110110100010101100000010','0100110101010100100101110','0010110101010110100001010','0111110100010101100101110','0000110100100100110001010','0011100110010011000101010','0101110100100101100001000','0110110001000010110001010','0110110001010011110001010','0011100010000101000101010','0010100010010011000101010','0100110010010001000000100','0111110011010101010000110','0000110100010100100100110','0100110100110101000101010','0100110100100001000001000','0101100010010101010100110','0111100011010101010101110','0101110001110011100001010','0101110110010111000101010','0101110001110001110001010','0101110101110101010001010','0010110000000100100100110','0101110001000111110001010','0101110101100000100001010','0111110010010101010001100','0100110100100000110001000','0101110100100001100101000','0111110010000111010101010','0001110001110001010001010','0101110100100100110001000','0101100010100101010001010','0100110100110000100001000','0000110100110100110001010','0100100010110001010001000','0111110101010100100001010','0001110110000111000101010','0100100111100101010001010','0101100110110101010001010','0011110001010011110001010','0101110010000111010101010','0100110101100001010000010','0111110001010110100001010','0011110001000100100101110','0100110100110000100001010','0111110100010100100101110','0101110100010101100000110','0010110101010100100001110','0100110100110001100001010','0001110100100001000101000','0001100010100001000101010','0100110101110101010001010','0010100011010001000101110','0101110100100100100001000','0101110100110101010101000','0010100010010101010000110','0100110100110001000001000','0001110010100111010101010','0011110001000011110001010','0001110000110001010000010','0100110101110111100001010','0101110001110011110001010','0011110100010101100000100','0000110100010101100101100','0101110001010101110000110','0110110101010111110001010','0110110100010101100001110','0100110101110110110001010','0011100010010101010000100','0000110011010001000100110','0010110110000111000101010','0101110101010010100001010','0100110100110000110000010','0011110010000111000101010','0101110011010101010000110','0101110100110001110001010','0001110100100101010101010','0100110101010100100001010','0101110010010101010100110','0001110101100001010001010','0101110111110101010001010','0101110100100001110101010','0100110100100101000101000','0011110100010100100101110','0010110100010100100100110','0101110100010101100101100','0001110111110101010000010','0100110100110101010101010','0101110101010100100001110','0110100110000011000101010','0100110100110001010000010','0111110001000010100001010','0100110100110100110101010','0001100110110101010000010','0111110101010101100001100','0001100110110001010000010','0101100011110101010000010','0001110100110101000101000','0111110001000111100001010','0001110011110101010000010','0001110100010101100000100','0100110100100011110000010','0001110110110001010000010','0111110101010100100001100','0101100010010101010001100','0001100010110101000101010','0110110101010010110001010','0101110100110100110001000','0001110010000011000101010','0101100010100001010000010','0101110001010110100001010','0100110101100000100001010','0100110100100001110001000','0001110000110101010000010','0101110001010101110000100','0100110101100100100001010','0001110100110000100101010','0000100010010101010001110','0100110001010000100001010','0001110000010010110000010','0101110100110000110101000','0000100110110101010001010','0100110101100101010001010','0000100011010101010100110','0101110100100001000101010','0001110100100001010101010','0101110100110000100000010','0000110101010101100101100','0111110101010101100101110','0100110101110000110001010','0101110101100010110001010','0001110001010101010100110','0101100110110011000101010','0100110100110101000101000','0010110110000011000101010','0010100011010101010000110','0111100011010101010000110','0000110100010100100000100','0100100110110000010001000','0100110100100101100001000','0110100011010101010000110','0101110100110100100101000','0111110100010101100000010','0111100011010101010001100','0101110010100111010101010','0001110010100011000101010','0110110001010011100001010','0010100011010101010101110','0001110111100101010000010','0101110101100101010001010','0001100010000011000101010','0101110010010101010101010','0001100100100101010000010','0011100010010101010101010','0101110100110001000101000','0010110100010101100101100','0101100110110001010001010','0001100100100001010000010','0000110100110000100101010','0001110100100101000101000','0110110100010101100000100'] 

samplesize = len(data)
output = [['',[],[],[],[]] for x in range(samplesize)]        #[network, point attractors, cycle attractors, posterior result, anterior result]

for m in range(samplesize):
	b = data[m]	  
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