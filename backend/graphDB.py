from py2neo import Graph, Node, Relationship
import math, random
from numpy import genfromtxt
import json

graph = Graph()
sizeofGraph = 10000



# add this to the node class ??



def delRel(name1, name2, relName) :
	qry = "MATCH (n:Song)-[rel:" + relName + "]->(n2:Song) AND n.name=\"" + name1 + "\" AND n2.name=\"" + name2 + "\" DELETE rel"
	graph.cypher.execute(qry)
	print "deleted relationship between " + name1 + " and " + name2


# Function: addRel()
# Args: 2 node name strings, and the similarity float

# creates an undirected relationship between the two nodes and lists the similarity
# as the property of the relationship.
# neo4j does not support undirected creations, thus had to establish work around
# by adding an inverted relationship. Can do this because the similarity between two
# songs is identical no matter which one comes first in the arguments.
def addRel(seed, node, sim):
	_n1 = search(seed); _n2 = search(node)
	rel = Relationship(_n1.node(), "SIM", _n2.node(), value=sim)
	rel2 = Relationship(_n2.node(), "SIM", _n1.node(), value=sim)
	graph.create(rel, rel2)		
		

# Function: escapeQuotes()
# Args: A song name, which is a string

# escapes any quotes in the song name so that it does not break the query
# returns a string
def escapeQuotes(name) :

	n = name.split('"')
	s = ""
	for i in range(len(n)-1):
		s += n[i] +  '\\\"'
	s += n[len(n)-1]
	return s

# Function: simRels()
# Args: a song name

# Two ways to do this. Can create paths through our database which do things based
# on key. OR. Can just use a filter on the compare function, where if the key 
# is not one of the similar ones, it is thrown out and not computed on. 

# for now going with second solution. 

# Gets a list of songs using the function narrowSearch, and creates a 
# "KEYSIM" relationship with those songs, connecting them in our database
# and allowing for faster compare times during runtime operations.

def simRels(name) :	
	songs = narrowSearch(name)
	name = escapeQuotes(name)
	
	qry = "MATCH (n:Song) WHERE n.name=\"" + name + "\" RETURN n"
	mainNode = graph.cypher.execute(qry)

	#for song in songs :
	song = songs[0]
	print song	
	song = escapeQuotes(song)
	qry = "MATCH (n:Song) WHERE n.name=\"" + song + "\" RETURN n"
	relNode = graph.cypher.execute(qry)
	rel = Relationship(mainNode[0][0], "KEYSIM", relNode[0][0])
	graph.create(rel)		
	
	

# Function: narrowSearch()
# Args: a name of a song for searching

# Takes in a target song, and returns all songs in the database with keys
# closely related to the target song.

# Need to do this to narrow the search for similar songs in database because
# we do not want to compare with everything in the database!

# returns a list of the songs similar to a seed song via key
def narrowSearch(name):
	songs = []; keys = []
	seed = search(name)	
	
	keys.append(seed.key())	
	keys.append((seed.key() + 7) % 12)
	keys.append((seed.key() + 5) % 12)

	for k in keys :
		songs = songs + searchGraph(0, sizeofGraph, key=k)
	
	return songs

# Function: getAll()

# Gets all song names in current database

# returns list of all songs in graph
def getAll() :
	songs = []

	qry = "MATCH (n:Song) RETURN n.name"
	ret = graph.cypher.execute(qry)
	
	for i in ret: 
		songs.append(i[0])
	return songs	


# Function: searchRandom()
# Args: the number of nodes desired

# randomizes numbers over the size of the entire neo4j database
# gathering random songs. When you query a list, it returns the same
# songs each time, so want to get a random smattering. 

# can update to check unique values by updating a table.

# returns a randomized list of songs. 

def searchRandom(_rVal) :
	songs = []
	songList = getAll()
	
	for i in range(_rVal) :
		num = random.randrange(len(songList))
		songs.append(songList[num])
	
	return songs

# class : search
# keeps a set of accessors for each of the nodes in our neo4j database
# allows for faster search and access results as well as lowering memory
# usage

# consider putting the parseTimbre function here.
class search :
	def __init__(self, name) :
		self.name = name
		self.cypherName = self.__escapeQuotes()
	def __escapeQuotes(self) :
		n = self.name.split('"')
		s = ""
		for i in range(len(n)-1):
			s += n[i] +  '\\\"'
		s += n[len(n)-1]
		return s
	def __cypherQuery(self, metric) :
		qry = "MATCH (n:Song) WHERE n.name=\"" + self.cypherName + "\" RETURN n." + metric
		ret = graph.cypher.execute(qry)
		return ret[0][0]
	def timbre(self) :
		return self.__cypherQuery("segmentTimbre")
	def tempo(self) : 
		return self.__cypherQuery("tempo")
	def pitch(self) :
		return self.__cypherQuery("segmentPitches")
	def beats(self) :
		return self.__cypherQuery("beatsStart")
	def key(self) :
		return self.__cypherQuery("key")
	def loudness(self) : 
		return self.__cypherQuery("segmentLoudness")
	def name(self):
		return self.name
	def node(self):
		qry = "MATCH (n:Song) WHERE n.name=\"" + self.name + "\" RETURN n"
		return graph.cypher.execute(qry)[0][0] 
 	# can add more as I use them		



# Function: searchString
# matches a metric with a string value (name, artist, genre)

# Returns results of cypher query

def searchString(_metric, _str, _rVal):
	query = "MATCH (n:Song) WHERE n." + _metric + " = \"" + _str + "\" RETURN n.name LIMIT " + str(_rVal) 
	return graph.cypher.execute(query)[0][0]


# Function searchNum
# matches metric and value exactly if it is a number value

# Returns results of a cypher query

def searchNum(_metric, _val, _rVal):
	query = "MATCH (n:Song) WHERE n." + _metric + " = " + str(_val) + " RETURN n.name LIMIT " + str(_rVal) 
	return graph.cypher.execute(query)

# Function: searchRange
# matches a range of values. Variance is passed in and the min/max are computed
# inside the function

# Returns results of a cypher query

def searchRange(_metric, _val, _rVal, _var):
	_minVal = _val - _var
	_maxVal = _val + _var
	query = "MATCH (n:Song) WHERE n." + str(_metric) + " > " + str(_minVal) + " AND n." + str(_metric) + " < " + str(_maxVal) + " RETURN n.name LIMIT " + str(_rVal)
	return graph.cypher.execute(query)[0]


# Function: searchMultiple(queryInfo, _rval)
# params:
#	queryInfo - A list of dictionaries holding values for the metric, the value of the metric,
#				and the variance on the value
#	_rval - number of results to return 
#
# Returns results of a cypher query matching all of the queryInfo list items
# If no nodes found for the query, returns None
def searchMultiple(queryInfo, _rval):
	query = "MATCH (n:Song) WHERE"
	for i in queryInfo:
		# queryInfo consists of raw values of:
		#	metric, val, rval, var 	
		if i['var'] != 0:
			_minVal = str(i['val'] - i['var'])
			_maxVal = str(i['val'] + i['var'])
			query = query + " n." + i['metric'] + " > " + _minVal + " AND n." + i['metric'] + " < " + _maxVal
		else:
			query = query + " n." + i['metric'] + " = " + str(i['val'])
		query = query + " AND"  
		
	query = query[:len(query) - 4]
	query = query + " RETURN n.name LIMIT " + str(_rval)
	ret = graph.cypher.execute(query)
	if len(ret) == 0: 
		return None
	songs = []
	for i in ret :
		songs.append(i[0])
	return songs
# prints the song names from a list of neo4j nodes
def printSong(songList):
	for song in songList :
		print song.n["name"]

# Function: searchGraph(kwargs)
# searches the neo4j database depending on the arguments given. 
# Arguments are passed at the function call
# Currently 3 cases:
# 	1 - String search: matches a given string directly (name, artist, genre)
#	2 - Single value search: matches the given value directly (key, timeSig)
#	3 - Range search: matches value within a given variance (tempo, keyConf, duration)

# Returns the results of the cypher query
# Return form is a list of lists of the results of the cypher queries
# the key for the list depends on where the metric is placed in the input argument
# string. 

# Example: searchGraph(0,1,key=5) will return a list of two lists. One of the result
#		   of the cypher query for key. The other a list of all combined search metrics.
#		   in this case, it will be an identical list. 

def searchGraph(var, rVal, **kwargs):
	# add in functionality to allow someone to set _var, and _rval from call
	# for now just setting in the function itself
	# all kwargs given MUST be in the form of the neo4j database!!!
	totalQueries = []

	if len(kwargs) != 0:
		for metric, value in kwargs.iteritems():
			qInf = { 'metric' : metric, 'val' : value, 'var' : 0 }
			#print "------" + metric + "-----"
			if metric == 'name':
				songList = searchString(metric, value, rVal)
			elif metric == 'key' or metric == 'timeSig':
				totalQueries.append(qInf)
			else:
				qInf['var'] = var
				totalQueries.append(qInf)
		if len(totalQueries) != 0: 
			songList = searchMultiple(totalQueries, rVal)
		return songList
	
	# base case match - no kwargs given
	return searchRandom(rVal)	




# Test function calls: 
#asdf = searchGraph(key=4, duration=250, tempo=120)
