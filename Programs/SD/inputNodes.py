import simplejson as json
import os,  fnmatch
from py2neo import Graph, Node, Relationship

graph = Graph() #creating graph object

#dictionary to hold all song info
#keys are: tags - sets of 2, [0] refers to the tag name, [1] refers to the tag strength (0-100)
#		   artist - holds artist name
#		   similars - holds a list of simliar songs, 
#					  [0] refers to track id, [1] refers to similarity rating (0-1)
#		   title - holds song name 
#		   track_id - holds track id (unique identifier) 
#		   timestamp - holds the timestamp of the release of the song 
#		   added - a boolean value which denotes if the song has been added to the dataset
list_of_songs = {} 

#dictionary to hold all song info
# path for files which is passed into get_file function. Make sure this points to the
# outer directory of thes songs you want to add. Also make sure that you are adding
# json files and else the get_file will return nothing
path = "/Users/Sonata/Downloads/lastfm_subset"

# a simlarity threshold that can be set here to manipulate which similarity relationships
# are created. 
similarity_threshold = 0 




#helper file for the file IO in add_rels and add_nodes
def openJSONFile(loc):
	fp = open(loc, "r")
	line = fp.readline()
	song = json.loads(line)
	fp.close()
	return song

#adds a song to the graph 
#pre: json already parsed and put in object using simplejson
#post: adds the song to the local neo4j database as well as creates relationships to all 
#	   similar tracks
def create_nodes(start_id):
	global similarity_threshold
	
	'''
	'''

	song = list_of_songs[start_id]
	if song != None:
		if start_id in list_of_songs.keys() :
			addSong = list_of_songs[start_id]['Node']
		for sim in song['similars'] :
			if sim[1] > similarity_threshold :
				if sim[0] in list_of_songs :
					linkNode = list_of_songs[sim[0]]['Node']
					rel = Relationship(addSong, "SIM TO", linkNode, degree=sim[1])
					graph.create(rel)

		
				


# adds all songs in all directories to a global dictionary list_of_songs
def add_nodes(basedir, ext='.json'):
	fter = '*'+ext	
	ctr = 0
	for root, dirs, files in os.walk(basedir):
		if ctr == 0: 
			print "adding files in " + ', '.join(dirs)
			ctr += 1	
		for f in fnmatch.filter(files, fter):
			loc = os.path.join(root, f) #file path
			song = openJSONFile(loc)
			song['added'] = False
			song['Node'] =  Node("Song", name=song['title'],
								artist=song['artist'], ID=song['track_id'])
			list_of_songs[song['track_id']] = song


# Main 
add_nodes(path)
print "all nodes added to dictionary" 
songs = list_of_songs.keys()
for song in songs :
	create_nodes(song)
print "all songs added to database with similarity relationships"
#end Main
