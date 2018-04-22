from . import auth
from . import users


def routes(params):
    return [
        (r'/v1', users.Hello),

        (r'/v1/auth', auth.Authorize, params),
        (r'/v1/auth/tokens', auth.Tokens, params),

        (r'/v1/users', users.AddUser),
        (r'/v1/users/([0-9]+)', users.GetUser),
    ]
