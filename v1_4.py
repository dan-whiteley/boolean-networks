'''
V1 - returns first successful network
V1_1 - estimates proportion of successes
V1_2 - returns list of every success (will take 100 hours)
V1_3 - look at whole state space for one solution
V1_4 - put em all together and churn out lots of graphs

'''
import numpy as np 
import matplotlib.pyplot as plt

#DRAW TREES FUNCTION

def tree(base,graph,cycle,bias):
	#find parents
	parents = graph[base][0]
	for each in cycle:
		if each in parents:
			parents.remove(each)


	#add parents to visits
	for a in parents:
		visits.append(a)

	#add co-ordinates to graph array
	l = len(parents)
	count = 0
	amp = graph[base][2][0]
	min_ang = graph[base][2][1]
	max_ang = graph[base][2][2] 

	for b in parents:
		graph[b][2][0] = amp + 1
		graph[b][2][1] = min_ang + count*(max_ang-min_ang)/l
		graph[b][2][2] = min_ang + (count+1)*(max_ang-min_ang)/l
		count = count + 1


	#draw
	for c in parents:
			mid = (graph[c][2][1] + graph[c][2][2])/2
			xco = graph[c][2][0]*np.cos(np.radians(mid))
			yco = graph[c][2][0]*np.sin(np.radians(mid)) + bias
			graph[c][2][3] = xco 
			graph[c][2][4] = yco
			plt.plot(xco,yco,'o',markersize=4)					
			plt.arrow(xco, yco, graph[base][2][3]-xco, graph[base][2][4]-yco, head_width=0.01, head_length=0.01, fc='k', ec='k')


	for z in parents:
		tree(z,graph,parents,bias)

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


#loop over every selection
#This will take hundreds of hours

successes = []
state = range(2**24) 
np.random.shuffle(state)   #randomize the selection in case all the succesful networks are clustered together (may take too long to find the first success)

for n in state:
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


	#initial state, in future different options tried

	T = 20

	astate = np.zeros((T+1,10))
	astate[0,:] = [1,0,0,0,0,1,0,0,0,0]

	#Run the network
	for t in range(T):

		#generate lists of effecting bools for each variable
		bools = [[] for x in range(10)]

		for [x,y] in am:
			bools[x].append(astate[t,y])
		for [x,y] in nm:
			bools[x].append(1-astate[t,y])

		#the state at the next time step is the product of each list in bools
		for i in range(10):
			astate[t+1,i] = np.prod(bools[i])

	#same for posterior
	pstate = np.zeros((T+1,10))
	pstate[0,:] = [0,0,0,0,0,0,0,0,0,0]

	#Run the network
	for t in range(T):

		#generate lists of effecting bools for each variable
		bools = [[] for x in range(10)]

		for [x,y] in am:
			bools[x].append(pstate[t,y])
		for [x,y] in nm:
			bools[x].append(1-pstate[t,y])

		#the state at the next time step is the product of each list in bools
		for i in range(10):
			pstate[t+1,i] = np.prod(bools[i])


	if np.all(astate[T,:] == astate[T-1,:]) and np.all(astate[T,:5] == np.array([1.,0.,1.,0.,1.])) and np.all(pstate[T,:] == pstate[T-1,:]) and np.all(pstate[T,:5] == np.array([0.,1.,0.,1.,0.])):
		successes.append(n)
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



		#graph[n] gives the parent nodes, child nodes and co-ordinates for the nth node.
		#graph[n][2][0] gives polar amplitude, [1] is min angle, [2] is max angle, [3] is x, [4] is y
		graph = [[[],[],[0,0,0,0,0]] for x in range(1024)]

		targets = [int(z) for z in targets]

		for y in range(1024):
			graph[y][1] = targets[y]			#add child
			graph[targets[y]][0].append(y)		#add parent

		visits = []

		fig = plt.figure()
		ax = fig.gca()										
		plt.suptitle(n,fontsize=20)										
		
		plt.xticks([])													
		plt.yticks([])													

		while len(visits)<1024:

			#find where to start
			for q in range(1024):
				if not q in visits:
					break

			#find base nodes
			while not (q in visits):
				visits.append(q)
				q = graph[q][1]

			

			base = visits[visits.index(q):]

			#find co-ordinates of base nodes

			tot = len(base)
			count = 0

			for x in base:
				graph[x][2][0] = 1
				graph[x][2][1] = count*180/tot
				graph[x][2][2] = (count+1)*180/tot 
				count = count + 1

			#find max y-co for bias for next tree
			
			bias = graph[0][2][4]

			for node in graph:
				if node[2][4]>bias:
					bias = node[2][4]

			bias = bias + 4



			#draw
			plt.text(0,bias - 3,base)	  										
			circle = plt.Circle((0,bias),1, color='k', fill=False)		
			ax.add_artist(circle)										
			for x in base:
				mid = (graph[x][2][1] + graph[x][2][2])/2.
				graph[x][2][3] = graph[x][2][0]*np.cos(np.radians(mid))
				graph[x][2][4] = graph[x][2][0]*np.sin(np.radians(mid)) + bias
				plt.plot(graph[x][2][3], graph[x][2][4],'o')			


			for x in base:
				tree(x,graph,base,bias)

			#do it again for the next set



		#find max y and x to get axis right
		max_x = graph[0][2][3]
		max_y = graph[0][2][4]
			
		for node in graph:
			if node[2][4]>max_y:
				max_y = node[2][4]
			if node[2][3]>max_x:
				max_x = node[2][3]

		#save
		plt.axis([-max_x-1,max_x+1,0,max_y + 1])
		string = str(n) + '.png'
		plt.savefig(string)

print(successes)
		

