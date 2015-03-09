from py2neo import Graph, Node, Relationship
import math
from numpy import genfromtxt
import json

graph = Graph()

def cosSim(v1, v2):
	"""compute cosine similarity of v1 to v2: (v1 dot v1)/{||v1||*||v2||)"""
	_lenV1 = len(v1)
	_lenV2 = len(v2)
	minLen = 0
	if _lenV1 < _lenV2:
		minLen = _lenV1
	else:
		minLen = _lenV2
	sumxx, sumxy, sumyy = 0, 0, 0
	for i in range(minLen):
		x = v1[i]; y = v2[i]
		sumxx += x*x
		sumyy += y*y
		sumxy += x*y
   	return sumxy/math.sqrt(sumxx*sumyy)

def tempoDiff(_tempo1, _tempo2):
	retVal = (_tempo1 + _tempo2)/math.sqrt(_tempo1*_tempo2)
	return retVal


# ?? this function makes no sense other than to call cosSim
def beatSim(_vector1, _vector2, _tempo1, _tempo2):
	_simVal = (cosSim(_vector1, _vector2) * 1) + (tempoDiff(_tempo1, _tempo2) * 0)
	return _simVal


# Function: searchString
# matches a metric with a string value (name, artist, genre)

# Returns results of cypher query

def searchString(_metric, _str, _rVal):
	query = "MATCH (n:Song) WHERE n." + _metric + " = \"" + _str + "\" RETURN n LIMIT " + str(_rVal) 
	return graph.cypher.execute(query)


# Function searchNum
# matches metric and value exactly if it is a number value

# Returns results of a cypher query

def searchNum(_metric, _val, _rVal):
	query = "MATCH (n:Song) WHERE n." + _metric + " = " + str(_val) + " RETURN n LIMIT " + str(_rVal) 
	return graph.cypher.execute(query)

# Function: searchRange
# matches a range of values. Variance is passed in and the min/max are computed
# inside the function

# Returns results of a cypher query

def searchRange(_metric, _val, _rVal, _var):
	_minVal = _val - _var
	_maxVal = _val + _var
	query = "MATCH (n:Song) WHERE n." + str(_metric) + " > " + str(_minVal) + " AND n." + str(_metric) + " < " + str(_maxVal) + " RETURN n LIMIT " + str(_rVal)
	return graph.cypher.execute(query)



# Function: searchMultiple(queryInfo, _rval)
# params:
#	queryInfo - A list of dictionaries holding values for the metric, the value of the metric,
#				and the variance on the value
#	_rval - number of results to return 
#
# Returns results of a cypher query matching all of the queryInfo list items

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
	query = query + " RETURN n LIMIT " + str(_rval)
	return graph.cypher.execute(query)


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
def searchGraph(**kwargs):
	# add in functionality to allow someone to set _var, and _rval from call
	# for now just setting in the function itself
	# all kwargs given MUST be in the form of the neo4j database!!!
	_var = 5
	_rval = 10
	totalQueries = []
	if kwargs is not None:
		for metric, value in kwargs.iteritems():
			qInf = { 'metric' : metric, 'val' : value, 'var' : 0 }
			print "------" + metric + "-----"
			if metric == 'name':
				songList = searchString(metric, value, _rval)
				#printSong(songList)
			elif metric == 'key' or metric == 'timeSig':
				songList = searchNum(metric, value, _rval)
				totalQueries.append(qInf)
				#printSong(songList)
			else:
				songList = searchRange(metric, value, _rval, _var)
				qInf['var'] = _var
				totalQueries.append(qInf)
				#printSong(songList)	
		songList = searchMultiple(totalQueries, _rval)
		printSong(songList)
		return songList

# Test function calls: 
#asdf = searchGraph(key=4, duration=250, tempo=120)
