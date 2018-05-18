import json
from tornado.httputil import url_concat
from . import base
from ... import auth


class Authorize(base.BaseHandler):

    def auth_validate(self, uri, body, method, headers):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass

        scopes, credentials = auth.server.validate_authorization_request(
            uri, method,
            body, headers,
        )
        return scopes, credentials

    def auth_response(self, uri, scopes, credentials):
        headers, response, status = auth.server.create_authorization_response(
            uri=credentials["redirect_uri"],
            scopes=scopes,
            credentials=credentials
        )
        return headers, response, status

    async def get(self):
        if self.current_user:
            # Run blocking call on a separate thread.
            scopes, credentials = await self.application.run(
                self.auth_validate,
                self.request.uri,
                self.request.body,
                self.request.method,
                self.request.headers,
            )
            self.render('authorize.html', scopes=scopes, **credentials)
        else:
            # Redirect the user back to this page after logging in.
            args = [
                ('next', self.request.uri),
            ]
            self.redirect(url_concat(self.reverse_url('login'), args))

    async def post(self):
        if self.current_user:
            uri = self.get_argument('redirect_uri')
            scopes = self.get_arguments('scopes')
            credentials = dict(
                state=self.get_argument('state'),
                client_id=self.get_argument('client_id'),
                redirect_uri=uri,
                response_type=self.get_argument('response_type'),
            )
            # Run blocking call on a separate thread.
            headers, response, status = await self.application.run(
                self.auth_response,
                uri,
                scopes,
                credentials,
            )
            self.redirect(headers.get('Location', None))
        else:
            # Redirect the user back to this page after logging in.
            args = [
                ('next', self.request.uri),
            ]
            self.redirect(url_concat(self.reverse_url('login'), args))


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


class Login(base.BaseHandler):

    async def get(self):
        username = ''
        password = ''
        messages = None
        redirect = self.get_argument('next', self.reverse_url('auth'))
        self.render(
            'login.html',
            username=username,
            password=password,
            messages=messages,
            redirect=redirect,
        )

    async def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        redirect = self.get_argument('redirect')
        if username == 'hello@world.com' and password == 'abcdef':
            self.login_done(username, password, redirect)
        else:
            self.login_fail(username, password, redirect)

    def login_done(self, username, password, redirect):
        user = dict(
            id=123456,
            name='Hello World',
            email=username,
        )
        self.set_secure_cookie('user', json.dumps(user))
        self.redirect(redirect)

    def login_fail(self, username, password, redirect):
        messages = dict(
            login='Incorrect email address or password',
        )
        self.render(
            'login.html',
            username=username,
            password=password,
            messages=messages,
            redirect=redirect,
        )
