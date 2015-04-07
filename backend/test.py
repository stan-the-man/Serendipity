from py2neo import Graph, Node, Relationship
from machineAlgs import compare
from graphDB import searchGraph, simRels, getAll, narrowSearch
import random

# set the seed and stuff
song = "She Will Be Loved"
#stuff = getAll()
#stuff = searchGraph(0,1)
stuff = narrowSearch(song)
seed = searchGraph(0,1,name=song)

# simRels(song)


songsReturned = 15
ctr = 0	



while ctr < songsReturned:
	node = stuff[random.randrange(len(stuff)-1)]
	sim = compare(seed, node)
	ctr += 1
	node = node.encode('utf-8')
	print node + '\t' + str(sim)




#print len(stuff) - 1
#print random.randrange(len(stuff))


'''	
for node in stuff :
	node = node.encode('utf-8')
	sim = compare(seed, node)
	if sim != -1 :
		print node + '\t' + str(sim)
'''


#compare(stuff[0], seed)


