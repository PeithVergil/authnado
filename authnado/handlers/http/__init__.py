from tornado.web import url
from . import auth
from . import users


def routes(**kwargs):
    return [
        url(r'/v1', users.Hello),

        url(r'/v1/auth', auth.Authorize, kwargs, name='auth'),
        url(r'/v1/auth/login', auth.Login, name='login'),
        url(r'/v1/auth/tokens', auth.Tokens, kwargs, name='tokens'),

        url(r'/v1/users', users.AddUser),
        url(r'/v1/users/([0-9]+)', users.GetUser),
    ]
