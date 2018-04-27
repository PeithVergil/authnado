import json
from . import base
from ... import auth


class Authorize(base.BaseHandler):

    def validate(self, uri, body, method, headers):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass

        scopes, credentials = auth.server.validate_authorization_request(
            uri, method,
            body, headers,
        )
        return scopes, credentials

    async def get(self):
        # Run blocking call on a separate thread.
        scopes, credentials = await self.application.run(
            self.validate,
            self.request.uri,
            self.request.body,
            self.request.method,
            self.request.headers,
        )
        self.render('authorize.html', **credentials)

    async def post(self):
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
        status, headers, response = await self.application.run(
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
