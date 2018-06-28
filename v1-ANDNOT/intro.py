''' 
Essential idea is that n variables with binary states interact with each other according to boolean operators

The biological model to be built involves 24 interactions to select from on 10 variables, we'll start with a simple 9 on 3.

The interaction matrix (n x n) shows which operators apply.
In our case we only have ANDs (+), and NOTs (-)
Say a 3x3 matrix represents interactions between binary variables A, B and C
[[+, 0, -],
 [-, 0, 0],
 [0, -, +]]

The above matrix means that:
A(t+1) = A(t) AND NOT C(t)
B(t+1) = NOT A(t)
C(t+1) = NOT B(t) AND C(t)

We will want to iterate through many possible networks so there will be a 'fixed' matrix like above, and a 'selection' matrix
which will pick out which interations to apply. The two multiplied element-wise is the interaction matrix.

For ease of computation the interaction matrix can be split into an 'AND' matrix and a 'NOT' matrix, this also allows for generalisation to other operators later.
'''
import numpy as np 
import matplotlib.pyplot as plt

#initialise fixed matrix

fixed = np.array([[1,1,-1],[1,1,1],[1,-1,1]])

#initialise selection, in future version 2^9 options will be looped over

selection = np.array([[0,1,0],[0,0,1],[1,0,0]])

#find the interaction matrix

interaction = selection * fixed

#split into AND and NOT matrices

am = np.argwhere(interaction==1)  #[[0,0][1,1][2,2]]
nm = np.argwhere(interaction==-1) #[[1,2]] note empty dimension



#initial state, in future different options tried

T = 20

state = np.zeros((T+1,3))
state[0,:] = [0,1,1]

#Run the network
for t in range(T):

	#generate lists of effecting bools for each variable
	bools = [[] for x in range(3)]

	for [x,y] in am:
		bools[x].append(state[t,y])
	for [x,y] in nm:
		bools[x].append(1-state[t,y])

	#the state at the next time step is the product of each list in bools
	for i in range(3):
		state[t+1,i] = np.prod(bools[i])


plt.plot(state[:,0],state[:,1]*2 + state[:,2],markersize=2)
plt.axis([-1,2,-1,4])
plt.show()


	

