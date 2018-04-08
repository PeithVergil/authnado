from . import users


routes = [
    (r'/', users.Hello),
]
