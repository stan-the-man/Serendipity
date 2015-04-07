if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from reqHandler import api
	
    try:
        print('Visit http://localhost:8081/')
        make_server('', 8081, api).serve_forever()
    except KeyboardInterrupt:
        print('\nThanks!')
