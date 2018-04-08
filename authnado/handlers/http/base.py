import json
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def jsonify(self, data):
        self.write(json.dumps(data))
