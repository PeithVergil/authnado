import json
from tornado.httputil import url_concat
from . import base


class Authorize(base.BaseHandler):

    def initialize(self, **kwargs):
        self.auth = kwargs.get('provider')

    async def get(self):
        if self.current_user:
            scopes, credentials = await self.auth.validate_request(
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
            headers, response, status = await self.auth.create_response(
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

    def initialize(self, **kwargs):
        self.auth = kwargs.get('provider')

    async def post(self):
        headers, response, status = await self.auth.create_token(
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
