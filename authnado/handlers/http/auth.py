import json
from . import base
from ... import auth


class Authorize(base.BaseHandler):

    def get(self):
        self.set_status(201)
        self.jsonify(dict(
            name='auth.get'
        ))

    def post(self):
        self.jsonify(dict(
            name='auth.post',
        ))


class Tokens(base.BaseHandler):

    def post(self):
        uri, method = self.request.uri, self.request.method,
        body, headers = self.request.body, self.request.headers,

        body = json.loads(body)

        # Define extra credentials here.
        credentials = dict()

        headers, body, status = auth.server.create_token_response(
            uri, method,
            body, headers,
            credentials
        )
        self.set_status(status)
        for key, val in headers.items():
            self.set_header(key, val)
        self.write(body)
