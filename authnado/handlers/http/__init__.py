from . import auth
from . import users


routes = [
    (r'/v1', users.Hello),

    (r'/v1/auth', auth.Authorize),
    (r'/v1/auth/tokens', auth.Tokens),

    (r'/v1/users', users.AddUser),
    (r'/v1/users/([0-9]+)', users.GetUser),
]
