'''

now to try all possible selections 2^24

and collect all those where there is a steady state which matches the desired [1 0 0 0 0 1 0 0 0 0] to [1 0 1 0 1 .....] anterior, 
and [0*10] to [0 1 0 1 0 ......] posterior


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
#WARNING!!! On a basic laptop this will take 100 hours

successes = []

for n in range(2**24):
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
	astate[0,:] = [0,0,0,0,0,0,0,0,0,0]

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


print(successes)
print(len(successes))
		

