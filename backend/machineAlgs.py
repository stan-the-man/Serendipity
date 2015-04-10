import math
from multiprocessing import Process, Manager
from numpy import genfromtxt
from graphDB import search


# Idea for what to do:
# create a path for all these path thingies. Then find all the songs and randomize from
# list.

# also figure out which ones are computationally heavier and see if you need to do them
# or if you can infer similarity without them!


# Funtion: filterKey()
# Args: two song keys, one is the main key, the other the comparison key

# returns true if the key is the same or the relative minor/major, else false
def filterKey(key1, key2) :
	if key1 == key2 or key1 == ((key2 + 5) % 12) or key1 == ((key2 + 7) % 12):
		return True
	return False


# Function: parseTimbre()
# Args: the segmentTimbre input from a Node from neo4j

# I noticed that this was coming in the form of a string before, so this function
# parses that string, separates the values into their tuples, converts them to 
# floats, and then restructures the tuples into a list which can be run through
# cosSim.

# in neo4j database, timbre comes in form of array[segmentNumber][12] where each 
# segment number has a 12 tuple attached to it. 

# I essentially transpose this matrix to give an output form of array[12][segmentNumber] 

# Returns: list of timbre outputs. Keys are the 12 different tuples.

def parseTimbre(_tim):
	segmentTimbre = []
	timbre = []

	tim = _tim.split()
	# get everything into the form required 
	for i in tim :
		i = i.rstrip(',')
		if(i[len(i)-1] == ']') :
			i = i.rstrip(']')
			timbre.append(float(i))
			segmentTimbre.append(timbre)
			timbre = []	
		while i[0] == '[' :
			i = i.lstrip('[')
		timbre.append(float(i))

	# put each timbre section in a list with its compatriots.
	timbre = []
	ret = []
	for i in range(len(segmentTimbre[0])) : 
		for j in segmentTimbre :
			timbre.append(j[i])
		ret.append(timbre)
		timbre = []

	return ret


# cosine similarity helper function 
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
	if sumxx * sumyy == 0: 
		return 0
   	return sumxy/math.sqrt(sumxx*sumyy)

# computes the distance between two given values
# basic alg. Needs work probably. 
def singleDiff(_tempo1, _tempo2):
	_t1 = math.floor(_tempo1)
	_t2 = math.floor(_tempo2)
	if _t1 ==  _t2:
		return 1
	return 1 / math.sqrt((_t1 - _t2)**2)


# Function: beatSim()
# Args: the two beat vectors from beatsStart and the two tempo floats

# Preforms cosSim on the vector portion, and a distance algorithm for the tempo number

# Returns: similarity coeffcient from 0-1

def beatSim(_vector1, _vector2, _tempo1, _tempo2):
	_simVal = (cosSim(_vector1, _vector2) * .1) + (singleDiff(_tempo1, _tempo2) * .9)
	return _simVal


# Function: timbreSim()
# Args: two timbre features from the Node

# performs cosine sim on the timbre features and smoothes them according to 
# SOME FORM OF MATH HERE

# Returns: simliarity coefficient from 0-1

def timbreSim(_tim1, _tim2) :
	_simi = []
	t1 = parseTimbre(_tim1); t2 = parseTimbre(_tim2)
	
	_lenV1 = len(t1)
	_lenV2 = len(t2)
	minLen = 0
	if _lenV1 < _lenV2:
		minLen = _lenV1
	else:
		minLen = _lenV2
	
	for i in range(minLen) :
			_simi.append(cosSim(t1[i],t2[i]))
	
	# for now going to return the mean of the similarities.
	# leaving room to add extra smoothing if desired

	#_smoothing = [] # should have 12 values, one for each entry in the timbre tuple
	_ret = 0.0 
	for i in _simi :
		_ret = _ret + i	
	return _ret / 12     # instead of 12, can use len(_smoothing) when it has values

# Function: keySim()
# Args: 2 integers representing the key of the song, between 0-11

# uses circle of fiths, a basic music theory basis to similarize songs.
# essentially, the further the query song is from the data song on the circle 
# the less simliar it is. 

# Returns: similarity coefficient from 0-1. 

def keySim(_key1, _key2) :
	# cycle of fifths - all keys are reported in as a int between 0-11 (C, C#, D, ... ,B)
	# things are most similar to themselves, and keys that are +5 or +7 %12 
	# 5 correpsonds to the flat side, 7 to the sharp side

	# same key means supreme similarity
	if _key1 == _key2 :
		return 1
	
	sharp = _key1 
	flat = _key1
	cnt = 0
	while sharp != _key2 and flat != _key2 :
		sharp = (sharp + 7) % 12 
		flat = (flat + 5) % 12
		cnt = cnt + 1
	# cnt has number of cylces it took to find a similar key. 
	# 1 = very simliar, 5 = sort of similar, 12 = not similar at all
	# very rudimentary alg
	return (12 - float(cnt)) / 12

# Function: compare()
# Args: strings of names from 2 nodes from our neo4j library.
#		Prereq: Nodes much have data for segmentTimbre, beatsStart, tempo
#				segmentPitches, and segmentLoudness

# Takes in all args, compares them using cosine simliarity
# Special case: key - explained in keySim function

# Returns: a normalized similarity coefficient between 0 and 1

# Fang's suggestions: Z-scores, machine learning for optimal metric setting, 

def compare(_name1, _name2) :
	_n1 = search(_name1); _n2 = search(_name2)
	_results = []
	# check the key here.
	#if not filterKey(_n1.key(), _n2.key()) :
	#	return -1

	_timbre = timbreSim(_n1.timbre(), _n2.timbre())	 
	_beats = beatSim(_n1.beats(), _n2.beats(), _n1.tempo(), _n2.tempo())
	_key = keySim(_n1.key(), _n2.key())
	_pitch = cosSim(_n1.pitch(), _n2.pitch())	
	#_loudness = cosSim(_n1.loudness(), _n2.loudness())
	_loudness = 0
	# timbre, key, and pitch are the best metrics for evaluation. 
	# currently, beats and loudness are all close together for all songs	
	
	#print _timbre
	#print _beats
	#print _key
	#print _pitch

	
	_timbreSmoothing = .2
	_beatsSmoothing = .3
	_keySmoothing = .4
	_pitchSmoothing = .1
	_loudnessSmoothing = 0   

	return  _timbre * _timbreSmoothing + _beats * _beatsSmoothing + _key * _keySmoothing + _pitch * _pitchSmoothing + _loudness * _loudnessSmoothing


# Function: compareT()
# Args: 2 string names of songs

# This function calculates the simliarity between all the relevant metrics of the 
# song nodes in the neo4j database, and uses mulitprocessing to do the computation
# accross all available cores on the computer. 
# Currently running a 4 core MACbook laptop. 
# Did this to try and decrease the computation time for the similarity computations.
# and use computers cores more effectively. 

# Metrics: timbre, beats, tempo, key, pitch

# Returns a float value from 0-1 displaying the similarity between the two songs. 
# 1 being most similar, 0 being least. 
def compareT(name1, name2):
	_n1 = search(name1); _n2 = search(name2)

	manager = Manager()
	
	_timbre = manager.list([])
	_beats = manager.list([])
	_key = manager.list([])
	_pitch = manager.list([])
	_loudness = 0.0

	_timbreThread = Process(target=timbreSimT, args=(_n1.timbre(), _n2.timbre(), _timbre))
	_timbreThread.start(); #_timbreThread.join()
	
	_beatsThread = Process(target=beatSimT, args=(_n1.beats(), _n2.beats(), _n1.tempo(), _n2.tempo(), _beats))
	_beatsThread.start(); #_beatsThread.join()
	
	_keyThread = Process(target=keySimT, args=(_n1.key(), _n2.key(), _key))
	_keyThread.start(); #_keyThread.join()
	
	_pitchThread = Process(target=pitchSimT, args=(_n1.pitch(), _n2.pitch(), _pitch))
	_pitchThread.start(); #_pitchThread.join()
	
	_timbreThread.join()
	_beatsThread.join()
	_keyThread.join()
	_pitchThread.join()


	_timbreSmoothing = .2
	_beatsSmoothing = .3
	_keySmoothing = .4
	_pitchSmoothing = .1
	_loudnessSmoothing = 0   

	return  _timbre[0] * _timbreSmoothing + _beats[0] * _beatsSmoothing + _key[0] * _keySmoothing + _pitch[0] * _pitchSmoothing + _loudness * _loudnessSmoothing


# Thread Similarity Helper functions: 

# below are helper functions for the compareT function
# the each use the similarity functions defined above, but
# save the results in a list for pass-by-reference output for the threads
# since Process class cannot return results (or I at least do not know how to do that)

def keySimT(k1, k2, res):
	res.append(keySim(k1, k2))
	
def timbreSimT(t1, t2, res) :
	res.append(timbreSim(t1, t2))

def beatSimT(b1, b2, t1, t2, res) :
	res.append(beatSim(b1, b2, t1, t2))

def pitchSimT(p1, p2, res) :
	res.append(cosSim(p1, p2))

