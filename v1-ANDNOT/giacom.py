'''
See intro.py for the basics of the implementation

This extends the 9-interaction case to the 24 interactions between 10 variables to reproduce Giacomantonio et al 2010

Other additions will include:
-that multiple selections will be tried
-that there will be two state vectors, the anterior and posterior

It differs from Giacomantonio in that the update will not be asynchronous or stochastic

The indexes of the variables from 0-9:
Fgf8 gene
Emx2 ''
Pax6
Coup-tfi
Sp8
Fgf8 protein
Emx2 ''
and so on

The initial state would be [1,0,0,0,0,1,0,0,0,0] in anterior, and 0 in posterior
although robustness under other initial states would be interesting to look at

The desired anterior steady state includes [1,0,1,0,1...], 
and the opposite for posterior, [0,1,0,1,0...] as these represent opposing gradients

Some interactions that will always be selected include 'Sp8 prot activates Fgf8 gene', and 'X gene causes x prot'

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



#initialise selection
#This is the 'hypothesised' selection which Giacom disproves [[1,1,0,0,1],[1,0,1,1,1],[0,1,0,1,1],[1,0,0,0,1],[1,1,0,0,0]]
#other selections: Giacomantonios 2 best:
#[[0,0,0,0,1],[1,0,1,0,0],[1,0,0,1,0],[1,0,1,0,1],[0,1,0,1,0]] or
#[[0,0,0,0,1],[1,0,1,0,1],[1,1,0,0,0],[1,0,1,0,1],[0,1,0,1,0]]
selection = np.ones((10,10))
selection[0:5,5:10]=[[0,0,0,0,1],[1,0,1,0,1],[1,1,0,0,0],[1,0,1,0,1],[0,1,0,1,0]]



#find the interaction matrix

interaction = selection * fixed

#split into AND and NOT matrices

am = np.argwhere(interaction==1) 
nm = np.argwhere(interaction==-1) 


#initial state, for posterior try zeros(10), for anterior - [1,0,0,0,0,1,0,0,0,0]

T = 20

state = np.zeros((T+1,10))
state[0,:] = [0,0,0,0,0,0,0,0,0,0]

#Run the network
for t in range(T):

	#generate lists of effecting bools for each variable
	bools = [[] for x in range(10)]

	for [x,y] in am:
		bools[x].append(state[t,y])
	for [x,y] in nm:
		bools[x].append(1-state[t,y])

	#the state at the next time step is the product of each list in bools
	for i in range(10):
		state[t+1,i] = np.prod(bools[i])

print state
#The plot below is to show evolution in state space, with markers on the final states to show direction in time
plt.plot(state[:,0] + state[:,1]*2 + state[:,2]*4 + state[:,3]*8 + state[:,4]*16, state[:,5] + state[:,6]*2 + state[:,7]*4 + state[:,8]*8 + state[:,9]*16 )
plt.plot(state[5:,0] + state[5:,1]*2 + state[5:,2]*4 + state[5:,3]*8 + state[5:,4]*16, state[5:,5] + state[5:,6]*2 + state[5:,7]*4 + state[5:,8]*8 + state[5:,9]*16 ,'o' )
plt.axis([-1,32,-1,32])
plt.show()
	
'''
RESULTS

Test			Ant 1 -> 1 0 1		Post 0 -> 0 1 0

hypothesised	no,opposite			yes!

Giacom 1		yes!				opposite

Giacom 2		yes!				opposite
'''
