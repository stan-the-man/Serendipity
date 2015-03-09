import math
from numpy import genfromtxt

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
   	return sumxy/math.sqrt(sumxx*sumyy)

# computes the distance between two given values

def singleDiff(_tempo1, _tempo2):
	retVal = (_tempo1 + _tempo2)/math.sqrt(_tempo1*_tempo2)
	return retVal


# Function: beatSim()
# Args: the two beat vectors from beatsStart and the two tempo floats

# Preforms cosSim on the vector portion, and a distance algorithm for the tempo number

# Returns: similarity coeffcient from 0-1

def beatSim(_vector1, _vector2, _tempo1, _tempo2):
	_simVal = (cosSim(_vector1, _vector2) * 1) + (singleDiff(_tempo1, _tempo2) * 0)
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
# Args: 2 nodes from our neo4j library.
#		Prereq: Nodes much have data for segmentTimbre, beatsStart, tempo
#				segmentPitches, and segmentLoudness

# Takes in all args, compares them using cosine simliarity
# Special case: key - explained in keySim function

# Returns: a normalized similarity coefficient between 0 and 1
def compare(_n1, _n2) :
	_timbre = timbreSim(_n1["segmentTimbre"], _n2["segmentTimbre"])
	_beats = beatSim(_n1["beatsStart"], _n2["beatsStart"], _n1["tempo"], _n2["tempo"])
	_key = keySim(_n1["key"], _n2["key"])
	_pitch = cosSim(_n1["segmentPitches"], _n2["segmentPitches"])
	_loudness = cosSim(_n1["segmentLoudness"], _n2["segmentLoudness"])

	_timbreSmoothing = .2
	_beatsSmoothing = .2
	_keySmoothing = .2
	_pitchSmoothing = .2
	_loudnessSmoothing = .2

	return _timbre * _timbreSmoothing + _beats * _beatsSmoothing + _key * _keySmoothing + _pitch * _pitchSmoothing + _loudness * _loudnessSmoothing


