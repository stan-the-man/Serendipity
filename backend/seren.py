# things.py

# Let's get this party started
import falcon, os, logging
from py2neo import Graph, Node, Relationship
try: 
    import ujson as json
except:
    import json

from mediSearch import MediaSearchResource
from textSearch import TextSearchResource
from userResponse import UserResponseResource

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class ThingsResource:
    def __init__(self, gdb):
        self.gdb = gdb
        self.logger = logging.getLogger('mediyak.' + self.__class__.__name__ )

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


# create logger with 'spam_application'
logger = logging.getLogger('Seren')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('seren.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('')
logger.info('==================== Serendipity Start ====================')
logger.info('')

logger.info('Initializing py2neo interface for Neo4j.')
gdb = Graph()
if gdb is None:
    logger.error('py2neo wrapper failed to initialize.')
    raise Exception('py2neo initialization failure.')

logger.info('Creating Falcon Resource objects.')
# Resources are represented by long-lived class instances
things = ThingsResource(gdb)
media = MediaSearchResource(gdb)
text = TextSearchResource(gdb)
user = UserResponseResource(gdb)

logger.info('Creating WSGI application.')
# falcon.API instances are callable WSGI apps
app = falcon.API()

# things will handle all requests to the '/things' URL path
app.add_route('/things/{filename}', things)         #testing shit
app.add_route('/media/{stuffhere}', media)          #pass filename on server?
app.add_route('/text/{searchstrings?}', text)       #pass search strings
app.add_route('/user/{stuffhere}', user)            #update precision calcualtions w/ user data

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8081/')
        make_server('', 8081, app).serve_forever()
    except KeyboardInterrupt:
        print('\nThanks!')
    logger.info('')
    logger.info('==================== Seren End ====================')
    logger.info('')
