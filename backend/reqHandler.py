import os
import time
import uuid
from getFeatures import getBeats, getTuning, getMFCC
from graphDB import searchGraph #, graphSim

import falcon

#path = "/Applications/mampstack-5.4.37-0/apache2/htdocs/seren/upload/"

api = application = falcon.API()

def _media_type_to_ext(media_type):
    # Strip off the 'song/' prefix
    return media_type[5:]


#relate this to MSD track ID form
def _generate_id():
    return str(uuid.uuid4())


class Resource(object):

    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_post(self, req, resp, filename):
			# Take in file name. Search for file in song directory
			# Run diagnostics on that found file
			# Return a list of similar songs
			

			# songName = req.stream.read(4096)
			# songName = songName.strip()
			# ext = '.mp3'
			# filename = songName + ext
			song_path = os.path.join(self.storage_path, filename)
			getBeats(song_path)
			
			#optimizer: open file once instead of multiple IO's?
			resp.status = falcon.HTTP_201
			resp.location = '/song_ids/'

		


		# with searchBPM(getBPM(song_id.ext)) as sim_songs

		
		# for s in sim_songs
			# print s
			# write to output
			# resp.body = resp.body + s + '\n'
			
		
		#if(req.query_string != ""):
			#parse query string for the info and generate cypher search strings
			"""
			queries = req.get_param_as_list(Search)
			
			exists = graphSearch(queries)
			if(exists):
				ret = graphSim(exists)

			resp.status = falcon.HTTP_201
			resp.body = ret
			"""

	def on_get(self, req, resp, filename) :
		# do what is in test.py
		# so for now. Getting random results... 
		# want to precompute top results??!?

				



song = Resource("/Users/Sonata/Programs/SD/post_req/")
#song = Resource(path)
# change this path to the one for the aws system (applications file)
api.add_route('/songs/{filename}', song)
api.add_route('/songs/{method}/{filename}', song)


# add full song and part song routes
# separate on_post request handlers for text entries
# 
