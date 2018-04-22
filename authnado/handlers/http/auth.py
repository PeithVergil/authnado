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

    def create(self, uri, body, method, headers):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass

        headers, response, status = auth.server.create_token_response(
            uri, method,
            body, headers,
        )

        return status, headers, response

    async def post(self):
        # Run blocking call on a separate thread.
        status, headers, response = await self.ioloop.run_in_executor(
            self.executor,
            self.create,
            self.request.uri,
            self.request.body,
            self.request.method,
            self.request.headers,
        )
        self.set_status(status)
        for key, val in headers.items():
            self.set_header(key, val)
        self.write(response)
