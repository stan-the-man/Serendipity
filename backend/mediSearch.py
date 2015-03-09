import falcon, os, logging, py2neo
from base64 import urlsafe_b64encode
try: 
    import ujson as json
except:
    import json

class MediaSearchResource(object):
	"""docstring for MediaSearchResource"""
	def __init__(self, gdb):
		self.gdb = gdb
        self.logger = logging.getLogger('Seren.' + self.__class__.__name__ )
	
	def on_get(self, req, resp, filename):
        print filename
        resp.status = falcon.HTTP_200  # This is the default status
        resp.set_header('Access-Control-Allow-Origin', '*')
        #resp.body = json.dumps( {"1": filename })
        resp.body = json.dumps({"niggers": filename})

    def on_post(self, req, resp, filename):
        #print "OKAY"
        #requestData = json.load(req.stream)
        print filename
        #print requestData
        #print "OKAY"
        #filename = requestData["filename"]
        #print "OKAY"
        #print filename
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.set_header('Access-Control-Allow-Origin', '*')
        #resp.body = json.dumps( {"1": filename })
        resp.body = json.dumps({"message": filename})